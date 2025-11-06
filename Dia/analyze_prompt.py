import re
import json

def extract_sections_and_count_words(file_path):
    """Extract sections from the system prompt and count words in each."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on headers (lines starting with #)
    sections = {}
    current_section = "Introduction"
    current_text = ""
    
    for line in content.split('\n'):
        if line.strip().startswith('#'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section
            current_section = line.strip().strip('# ').strip()
            current_text = ""
        else:
            current_text += line + "\n"
    
    # Save the last section
    if current_text.strip():
        sections[current_section] = current_text.strip()
    
    # Count words in each section
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_text in sections.items():
        words = re.findall(r'\b[a-zA-Z]+\b', section_text)
        word_count = len(words)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    return sections, section_word_counts, total_words

def identify_prompt_format(file_path):
    """Identify the format of the system prompt."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check for XML-like tags
    if re.search(r'<[^>]+>', content):
        return "Plain text with XML tags"
    
    # Check for markdown
    if re.search(r'^#{1,6}\s', content, re.MULTILINE):
        return "Plain text with Markdown"
    
    return "Plain text"

def extract_context_window_info(sections):
    """Extract context window information if present."""
    # Look for context window info in all sections
    for section_name, section_text in sections.items():
        # Look for common patterns
        patterns = [
            r'context\s+window.*?(\d+)',
            r'(\d+)\s+token',
            r'(\d+)\s+context',
            r'limit.*?(\d+)\s+token'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, section_text, re.IGNORECASE)
            if matches:
                return matches[0]
    
    return "Not specified"

def extract_rules(sections):
    """Extract rules from the prompt."""
    rules = []
    
    # Look for rules in sections with "rule" or "instruction" in the name
    for section_name, section_text in sections.items():
        if 'rule' in section_name.lower() or 'instruction' in section_name.lower():
            # Split into individual rules (look for numbered lists or bullet points)
            lines = section_text.split('\n')
            current_rule = ""
            
            for line in lines:
                if re.match(r'^\s*[\d]+[.)]\s', line) or re.match(r'^\s*[-*]\s', line):
                    if current_rule.strip():
                        rules.append(current_rule.strip())
                    current_rule = line
                else:
                    current_rule += " " + line
            
            if current_rule.strip():
                rules.append(current_rule.strip())
    
    return rules

def extract_workflow(sections):
    """Extract workflow information."""
    workflow = []
    
    # Look for workflow in sections with "workflow" or "process" in the name
    for section_name, section_text in sections.items():
        if 'workflow' in section_name.lower() or 'process' in section_name.lower() or 'step' in section_name.lower():
            # Look for numbered steps
            steps = re.findall(r'^\s*[\d]+[.)]\s+(.+)', section_text, re.MULTILINE)
            if steps:
                workflow.extend(steps)
    
    # If no explicit workflow found, look for any numbered steps in any section
    if not workflow:
        for section_name, section_text in sections.items():
            steps = re.findall(r'^\s*[\d]+[.)]\s+(.+)', section_text, re.MULTILINE)
            if steps:
                workflow.extend(steps)
                break
    
    return workflow

def extract_context_management(sections):
    """Extract context management information."""
    context_info = []
    
    # Look for context-related sections
    for section_name, section_text in sections.items():
        if 'context' in section_name.lower() or 'memory' in section_name.lower():
            context_info.append({
                'section': section_name,
                'content': section_text[:500] + '...' if len(section_text) > 500 else section_text
            })
    
    return context_info

def extract_coding_standards(sections):
    """Extract coding standards if present."""
    coding_info = []
    
    # Look for coding-related sections
    for section_name, section_text in sections.items():
        if 'code' in section_name.lower() or 'coding' in section_name.lower() or 'format' in section_name.lower():
            coding_info.append({
                'section': section_name,
                'content': section_text[:500] + '...' if len(section_text) > 500 else section_text
            })
    
    return coding_info

def extract_other_info(sections):
    """Extract other critical information."""
    other_info = []
    
    # Look for sections that don't fit other categories
    excluded_sections = ['overview', 'workflow', 'tool', 'context', 'rule', 'code', 'intro']
    
    for section_name, section_text in sections.items():
        should_include = True
        for excluded in excluded_sections:
            if excluded in section_name.lower():
                should_include = False
                break
        
        if should_include and len(section_text) > 100:  # Only include substantial sections
            other_info.append({
                'section': section_name,
                'content': section_text[:500] + '...' if len(section_text) > 500 else section_text
            })
    
    return other_info

if __name__ == "__main__":
    file_path = "Prompt.txt"
    
    # Extract sections and count words
    sections, section_word_counts, total_words = extract_sections_and_count_words(file_path)
    
    # Identify prompt format
    prompt_format = identify_prompt_format(file_path)
    
    # Extract context window info
    context_window = extract_context_window_info(sections)
    
    # Extract rules
    rules = extract_rules(sections)
    
    # Extract workflow
    workflow = extract_workflow(sections)
    
    # Extract context management
    context_management = extract_context_management(sections)
    
    # Extract coding standards
    coding_standards = extract_coding_standards(sections)
    
    # Extract other info
    other_info = extract_other_info(sections)
    
    # Prepare analysis data
    analysis_data = {
        "overview": {
            "total_words": total_words,
            "format": prompt_format,
            "context_window": context_window,
            "section_count": len(sections)
        },
        "sections": section_word_counts,
        "rules": rules[:10],  # Limit to first 10 rules
        "workflow": workflow[:10],  # Limit to first 10 steps
        "context_management": context_management,
        "coding_standards": coding_standards,
        "other_info": other_info
    }
    
    # Save analysis data to JSON file
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"=== SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Format: {prompt_format}")
    print(f"Context window: {context_window}")
    print(f"Sections: {len(sections)}")
    print()
    
    print("=== SECTION WORD COUNTS ===")
    for section, count in section_word_counts.items():
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        print(f"{section}: {count} words ({percentage:.1f}%)")
    
    print()
    print(f"=== RULES ({len(rules)} found) ===")
    for i, rule in enumerate(rules[:5], 1):  # Show first 5 rules
        print(f"{i}. {rule[:100]}{'...' if len(rule) > 100 else ''}")
    
    if len(rules) > 5:
        print(f"... and {len(rules) - 5} more rules")
    
    print()
    print(f"=== WORKFLOW STEPS ({len(workflow)} found) ===")
    for i, step in enumerate(workflow[:5], 1):  # Show first 5 steps
        print(f"{i}. {step[:100]}{'...' if len(step) > 100 else ''}")
    
    if len(workflow) > 5:
        print(f"... and {len(workflow) - 5} more steps")
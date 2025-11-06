import re
import json

def extract_sections_and_count_words(file_path):
    """Extract sections from the text system prompt and count words in each."""
    
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

def count_words_in_text(text):
    """Count words in a text."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_tools_info(sections):
    """Extract tools information from sections (if available)."""
    # For this prompt, tools are not explicitly defined in a separate section
    # We'll look for tool-related information in the content
    tools_info = []
    
    # Check if there are any tool references
    tool_mentions = []
    for section_name, section_text in sections.items():
        # Look for tool-related keywords
        if any(keyword in section_text.lower() for keyword in ['tool', 'command']):
            # Extract sentences that mention tools
            sentences = re.split(r'[.!?]+', section_text)
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in ['tool', 'command', 'function']):
                    tool_mentions.append({
                        'context_section': section_name,
                        'description': sentence.strip()
                    })
    
    return tools_info, len(tool_mentions)

def identify_workflow_steps(sections):
    """Identify workflow steps from the sections."""
    workflow_steps = []
    
    # Look for numbered lists or step-by-step instructions
    for section_name, section_text in sections.items():
        if 'workflow' in section_name.lower() or 'process' in section_name.lower():
            # Extract numbered steps
            lines = section_text.split('\n')
            for line in lines:
                # Look for numbered steps
                if re.match(r'^\s*\d+[\.\)]', line):
                    workflow_steps.append(line.strip())
    
    return workflow_steps

def extract_rules(sections):
    """Extract rules from the sections."""
    rules = []
    
    # Look for rule-like content (bulleted lists with imperative statements)
    for section_name, section_text in sections.items():
        if 'rule' in section_name.lower() or 'guideline' in section_name.lower():
            # Extract bulleted items
            lines = section_text.split('\n')
            for line in lines:
                if line.strip().startswith('-') and len(line.strip()) > 1:
                    # Check if it's an imperative statement (starts with verb)
                    rule_text = line.strip()[1:].strip()
                    if rule_text and rule_text[0].isupper():
                        rules.append({
                            'section': section_name,
                            'rule': rule_text
                        })
    
    return rules

def extract_context_management(sections):
    """Extract context management information."""
    context_info = []
    
    for section_name, section_text in sections.items():
        if 'context' in section_name.lower() or 'memory' in section_name.lower():
            context_info.append({
                'section': section_name,
                'content': section_text[:500] + "..." if len(section_text) > 500 else section_text
            })
    
    return context_info

def extract_coding_standards(sections):
    """Extract coding standards information."""
    coding_standards = []
    
    for section_name, section_text in sections.items():
        if 'coding' in section_name.lower() or 'style' in section_name.lower() or 'convention' in section_name.lower():
            coding_standards.append({
                'section': section_name,
                'content': section_text[:500] + "..." if len(section_text) > 500 else section_text
            })
    
    return coding_standards

if __name__ == "__main__":
    file_path = "google-gemini-cli-system-prompt.txt"
    
    # Extract sections and count words
    sections, section_word_counts, total_words = extract_sections_and_count_words(file_path)
    
    # Extract tools information
    tools_info, tool_mentions_count = extract_tools_info(sections)
    
    # For Gemini CLI, we can identify specific tools from the examples and mentions
    # Based on manual analysis, the tools mentioned are:
    # read_file, write_file, run_shell_command, glob, search_file_content, 
    # read_many_files, replace, list_directory, save_memory, git commands
    # But since the prompt doesn't explicitly define tools, we'll mark as unknown
    
    # Identify workflow steps
    workflow_steps = identify_workflow_steps(sections)
    
    # Extract rules
    rules = extract_rules(sections)
    
    # Extract context management info
    context_info = extract_context_management(sections)
    
    # Extract coding standards
    coding_standards = extract_coding_standards(sections)
    
    # Save analysis results
    analysis_result = {
        'total_words': total_words,
        'section_word_counts': section_word_counts,
        'sections': list(sections.keys()),
        'tools_count': tool_mentions_count,
        'workflow_steps_count': len(workflow_steps),
        'rules_count': len(rules)
    }
    
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, indent=2, ensure_ascii=False)
    
    print(f"=== SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Number of sections: {len(sections)}")
    print(f"Tool mentions: {tool_mentions_count}")
    print(f"Workflow steps identified: {len(workflow_steps)}")
    print(f"Rules identified: {len(rules)}")
    print()
    
    print("=== SECTION WORD COUNTS ===")
    for section, count in section_word_counts.items():
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        print(f"{section}: {count} words ({percentage:.1f}%)")
import re
import json

def extract_sections(text):
    """Extract major sections from the system prompt."""
    sections = {}
    
    # Find all headers (## or ###)
    header_pattern = r'^(#{2,3})\s+(.+)$'
    headers = re.finditer(header_pattern, text, re.MULTILINE)
    
    header_list = list(headers)
    
    # Extract content between headers
    for i, match in enumerate(header_list):
        level = len(match.group(1))
        title = match.group(2).strip()
        
        # Find the end of this section
        start_pos = match.end()
        if i < len(header_list) - 1:
            end_pos = header_list[i + 1].start()
        else:
            end_pos = len(text)
        
        # Extract content
        content = text[start_pos:end_pos].strip()
        
        # Store section
        sections[title] = {
            "level": level,
            "content": content
        }
    
    return sections

def analyze_qoder_prompt():
    """Analyze the Qoder system prompt files."""
    # Combine all prompt files
    combined_content = ""
    files = ["prompt.txt", "Quest Action.txt", "Quest Design.txt"]
    
    for file_name in files:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                combined_content += f"\n\n--- {file_name} ---\n\n" + content
        except FileNotFoundError:
            print(f"File {file_name} not found.")
    
    # Extract sections
    sections = extract_sections(combined_content)
    
    # Save sections to JSON
    with open("prompt_sections.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    
    # Print section titles
    print("Sections found in Qoder system prompts:")
    for title, data in sections.items():
        word_count = len(re.findall(r'\b\w+\b', data['content']))
        print(f"- {title} ({word_count} words)")
    
    return sections

def extract_workflow_steps(text):
    """Extract workflow steps from the prompt."""
    # Look for numbered lists or step-by-step instructions
    step_pattern = r'(?:\n|^)\s*(\d+)[\.\)]\s+([^\n]+)'
    steps = re.findall(step_pattern, text)
    
    return [{"step": int(num), "description": desc.strip()} for num, desc in steps]

def extract_rules(text):
    """Extract rules from the prompt."""
    # Look for rules in format "When X, do Y" or similar
    rule_patterns = [
        r'(?:when|if)\s+([^,\.]+)[,\s]+(?:then\s+)?([^\n\.]+)',
        r'(?:-|\*)\s*(.+?:\s*.+)',
        r'(?:rule|must|should|never|always)[\s:]+([^\n]+)'
    ]
    
    rules = []
    for pattern in rule_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                rules.append(f"{match[0]} → {match[1]}")
            else:
                rules.append(match)
    
    return list(set(rules))  # Remove duplicates

if __name__ == "__main__":
    sections = analyze_qoder_prompt()
    
    # Extract workflow from relevant sections
    workflow_sections = [title for title in sections.keys() if 'workflow' in title.lower() or 'planning' in title.lower() or 'step' in title.lower()]
    if workflow_sections:
        print("\nWorkflow-related sections:")
        for section in workflow_sections:
            print(f"- {section}")
    
    # Extract rules
    rules = []
    for title, data in sections.items():
        if 'rule' in title.lower() or 'guideline' in title.lower() or 'principle' in title.lower():
            section_rules = extract_rules(data['content'])
            rules.extend(section_rules)
    
    if rules:
        print(f"\nRules found: {len(rules)}")
        for rule in rules[:10]:  # Show first 10 rules
            print(f"- {rule}")
import re
import json
import os

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def extract_sections_and_content(file_path):
    """Extract sections from the system prompt text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on XML tags
    sections = {}
    tag_pattern = r'<(\w+)>(.*?)</\1>'
    matches = re.findall(tag_pattern, content, re.DOTALL)
    
    for tag, text in matches:
        section_name = tag.replace('_', ' ').title()
        sections[section_name] = text.strip()
    
    return sections

def get_file_format(file_path):
    """Get the format of the file based on its extension."""
    if file_path.endswith('.txt'):
        return 'Plain Text (XML Structure)'
    elif file_path.endswith('.json'):
        return 'JSON'
    elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
        return 'YAML'
    else:
        return 'Unknown'

def extract_role_and_identity(content):
    """Extract role and identity information."""
    # Look for core identity section
    identity_match = re.search(r'<core_identity>(.*?)</core_identity>', content, re.DOTALL)
    if identity_match:
        return identity_match.group(1).strip()
    return "Not specified"

def extract_workflow_steps(content):
    """Extract workflow steps from the content."""
    workflow_steps = []
    
    # Look for step-by-step instructions or workflows in various sections
    sections = re.findall(r'<(\w+)>(.*?)</\1>', content, re.DOTALL)
    
    for section_name, section_content in sections:
        # Look for list items in each section
        list_items = re.findall(r'[-•]\s+(.+)', section_content)
        for item in list_items:
            if len(item.strip()) > 10 and len(item.strip()) < 300:
                workflow_steps.append({
                    'section': section_name.replace('_', ' ').title(),
                    'step': item.strip()
                })
    
    return workflow_steps

def extract_rules(content):
    """Extract rules from the content."""
    rules = []
    
    # Look for rules (often in format "NEVER", "ALWAYS", "MUST")
    rule_indicators = [
        r'(NEVER\s+.+)',
        r'(ALWAYS\s+.+)',
        r'(MUST\s+.+)',
        r'(SHOULD\s+.+)'
    ]
    
    lines = content.split('\n')
    for line in lines:
        for pattern in rule_indicators:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                rule_text = match.strip()
                if len(rule_text) > 10 and len(rule_text) < 200:
                    # Find which section this rule belongs to
                    section = "General"
                    for sec_name, sec_content in re.findall(r'<(\w+)>(.*?)</\1>', content, re.DOTALL):
                        if rule_text in sec_content:
                            section = sec_name.replace('_', ' ').title()
                            break
                    rules.append({
                        'section': section,
                        'rule': rule_text
                    })
    
    return rules

def extract_context_management(content):
    """Extract context management information."""
    context_info = []
    
    # Look for context-related information in sections
    sections = re.findall(r'<(\w+)>(.*?)</\1>', content, re.DOTALL)
    
    for section_name, section_content in sections:
        if 'context' in section_name.lower() or 'memory' in section_name.lower():
            context_info.append({
                'section': section_name.replace('_', ' ').title(),
                'content': section_content.strip()
            })
    
    return context_info

def extract_coding_standards(content):
    """Extract coding standards or technical guidelines."""
    coding_standards = []
    
    # Look for technical guidelines
    sections = re.findall(r'<(\w+)>(.*?)</\1>', content, re.DOTALL)
    
    for section_name, section_content in sections:
        if 'technical' in section_name.lower() or 'coding' in section_name.lower() or 'code' in section_name.lower():
            coding_standards.append({
                'section': section_name.replace('_', ' ').title(),
                'content': section_content.strip()
            })
    
    return coding_standards

def extract_other_critical_info(content):
    """Extract other critical information."""
    other_info = []
    
    # Look for important sections that don't fit other categories
    sections = re.findall(r'<(\w+)>(.*?)</\1>', content, re.DOTALL)
    
    excluded_sections = ['core_identity', 'general_guidelines', 'technical_problems', 'math_problems', 
                        'multiple_choice_questions', 'emails_messages', 'ui_navigation', 'unclear_or_empty_screen', 
                        'other_content', 'response_quality_requirements']
    
    for section_name, section_content in sections:
        if section_name not in excluded_sections:
            other_info.append({
                'section': section_name.replace('_', ' ').title(),
                'content': section_content.strip()
            })
    
    return other_info

if __name__ == "__main__":
    # File paths
    default_prompt_file = "Default Prompt.txt"
    enterprise_prompt_file = "Enterprise Prompt.txt"
    
    # Check which files exist
    files_to_analyze = []
    if os.path.exists(default_prompt_file):
        files_to_analyze.append(default_prompt_file)
    if os.path.exists(enterprise_prompt_file):
        files_to_analyze.append(enterprise_prompt_file)
    
    for prompt_file in files_to_analyze:
        print(f"\n--- Analyzing {prompt_file} ---")
        
        # Count words in prompt file
        try:
            prompt_word_count = count_words_in_text(prompt_file)
            print(f"Words in prompt file: {prompt_word_count}")
        except Exception as e:
            print(f"Error counting words: {e}")
            prompt_word_count = 0
        
        # Get file format
        prompt_format = get_file_format(prompt_file)
        print(f"Prompt file format: {prompt_format}")
        
        # Extract sections
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sections = extract_sections_and_content(prompt_file)
            print(f"Number of sections in prompt: {len(sections)}")
            
            # Extract role information
            role_info = extract_role_and_identity(content)
            print(f"Role information: {role_info[:100]}...")
            
            # Extract workflow steps
            workflow_steps = extract_workflow_steps(content)
            print(f"Workflow steps: {len(workflow_steps)}")
            
            # Extract rules
            rules = extract_rules(content)
            print(f"Rules extracted: {len(rules)}")
            
            # Extract context management
            context_mgmt = extract_context_management(content)
            print(f"Context management sections: {len(context_mgmt)}")
            
            # Extract coding standards
            coding_standards = extract_coding_standards(content)
            print(f"Coding standards sections: {len(coding_standards)}")
            
            # Extract other critical info
            other_info = extract_other_critical_info(content)
            print(f"Other critical info sections: {len(other_info)}")
            
        except Exception as e:
            print(f"Error analyzing {prompt_file}: {e}")
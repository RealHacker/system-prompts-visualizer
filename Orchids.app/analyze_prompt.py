import re
import json

def analyze_decision_prompt(file_path):
    """Analyze the Decision-making prompt and extract key sections."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    analysis = {
        'role': '',
        'task': '',
        'tools': [],
        'rules': [],
        'cloning_instructions': ''
    }
    
    # Extract role
    role_match = re.search(r'<role>\s*(.*?)\s*</role>', content, re.DOTALL)
    if role_match:
        analysis['role'] = role_match.group(1).strip()
    
    # Extract task
    task_match = re.search(r'<task>\s*(.*?)\s*</task>', content, re.DOTALL)
    if task_match:
        analysis['task'] = task_match.group(1).strip()
    
    # Extract tools
    tools_match = re.search(r'<tools>\s*(.*?)\s*</tools>', content, re.DOTALL)
    if tools_match:
        tools_content = tools_match.group(1)
        tool_lines = tools_content.strip().split('\n')
        for line in tool_lines:
            if line.strip().startswith('- '):
                tool_desc = line.strip()[2:]  # Remove "- " prefix
                analysis['tools'].append(tool_desc)
    
    # Extract rules
    rules_match = re.search(r'<rules>\s*(.*?)\s*</rules>', content, re.DOTALL)
    if rules_match:
        rules_content = rules_match.group(1)
        rule_lines = rules_content.strip().split('\n')
        for line in rule_lines:
            if line.strip().startswith('- '):
                rule_desc = line.strip()[2:]  # Remove "- " prefix
                analysis['rules'].append(rule_desc)
    
    # Extract cloning instructions
    cloning_match = re.search(r'<cloning_instructions>\s*(.*?)\s*</cloning_instructions>', content, re.DOTALL)
    if cloning_match:
        analysis['cloning_instructions'] = cloning_match.group(1).strip()
    
    return analysis

def analyze_system_prompt(file_path):
    """Analyze the System Prompt and extract key sections."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    analysis = {
        'task_completion_principle': '',
        'preservation_principle': '',
        'navigation_principle': '',
        'error_fixing_principles': '',
        'reasoning_principles': '',
        'ui_ux_principles': '',
        'communication': '',
        'tool_calling': '',
        'best_practices': [],
        'tools': [],
        'critical_rules': []
    }
    
    # Extract principles
    principles = [
        'task_completion_principle',
        'preservation_principle',
        'navigation_principle',
        'error_fixing_principles',
        'reasoning_principles',
        'ui_ux_principles',
        'communication',
        'tool_calling'
    ]
    
    for principle in principles:
        pattern = f'<{principle}>(.*?)</{principle}>'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            analysis[principle] = match.group(1).strip()
    
    # Extract best practices sections
    best_practices_match = re.search(r'<best_practices>(.*?)</best_practices>', content, re.DOTALL)
    if best_practices_match:
        best_practices_content = best_practices_match.group(1)
        # Split by headings (lines starting with - or #)
        sections = re.split(r'\n\s*(?=- |\*)', best_practices_content)
        for section in sections:
            if section.strip():
                analysis['best_practices'].append(section.strip())
    
    # Extract tools
    tools_match = re.search(r'<tools>\s*(.*?)\s*</tools>', content, re.DOTALL)
    if tools_match:
        tools_content = tools_match.group(1)
        # Extract tool names (items in bullet points)
        tool_matches = re.findall(r'-\s+([a-zA-Z_]+):', tools_content)
        analysis['tools'] = tool_matches
    
    # Extract critical rules (items with **CRITICAL** or similar emphasis)
    critical_matches = re.findall(r'(\*\*CRITICAL[:\w ]*\*\*:?.*?(?:\n\s{2,}.*?)*?(?=\n\s*-|\n\s*\*\*|$))', content, re.DOTALL)
    analysis['critical_rules'] = [match.strip() for match in critical_matches]
    
    return analysis

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python analyze_prompt.py <prompt_type>")
        print("prompt_type: 'decision' or 'system'")
        sys.exit(1)
    
    prompt_type = sys.argv[1]
    
    if prompt_type == 'decision':
        analysis = analyze_decision_prompt('Decision-making prompt.txt')
    elif prompt_type == 'system':
        analysis = analyze_system_prompt('System Prompt.txt')
    else:
        print("Invalid prompt_type. Use 'decision' or 'system'")
        sys.exit(1)
    
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
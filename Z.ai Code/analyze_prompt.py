import re
import json
import os

def extract_sections_and_count_words(file_path):
    """Extract sections from the Z.ai system prompt and count words in each."""
    
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

def extract_tools(file_path):
    """Extract tools defined in the Z.ai system prompt."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    tools = []
    
    # Extract tools based on specific mentions in the prompt
    # Look for explicit tool mentions
    tool_patterns = [
        r'([A-Za-z_]+\s*/\s*[A-Za-z_]+)',  # Tools like TodoRead/TodoWrite
        r'`([a-z_]+)`\s+tool',  # Tools mentioned with backticks
        r'([A-Za-z_]+)\s+tool',  # General tool mentions
        r'z-ai-web-dev-sdk',  # Specific SDK
        r'Prisma ORM',  # Database tools
        r'shadcn/ui',  # UI components as tools
        r'socket\.io',  # Websocket tools
    ]
    
    # Find tools from the Important Rules section
    important_rules_match = re.search(r'# Important Rules(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if important_rules_match:
        rules_text = important_rules_match.group(1)
        # Extract tools from rules
        todo_matches = re.findall(r'([A-Za-z]+Read/[A-Za-z]+Write)', rules_text)
        tools.extend(todo_matches)
        
        write_file_matches = re.findall(r'`([a-z_]+)`\s+tool', rules_text)
        tools.extend(write_file_matches)
    
    # Find tools from the AI section
    ai_match = re.search(r'## AI(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if ai_match:
        ai_text = ai_match.group(1)
        if 'z-ai-web-dev-sdk' in ai_text:
            tools.append('z-ai-web-dev-sdk')
    
    # Find tools from other sections
    if 'Image Generation tool' in content:
        tools.append('Image Generation')
    
    if 'websocket/socket.io' in content.lower():
        tools.append('Socket.io')
    
    if 'prisma orm' in content.lower():
        tools.append('Prisma ORM')
    
    if 'shadcn/ui' in content.lower():
        tools.append('shadcn/ui Components')
    
    # Remove duplicates and return
    return list(set(tools))

def count_tools(file_path):
    """Count the number of tools defined in the system prompt."""
    tools = extract_tools(file_path)
    return len(tools)

def extract_key_info(file_path):
    """Extract key information from the Z.ai prompt."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract information about the agent
    info = {
        'role': '',
        'workflow_steps': [],
        'tools': [],
        'context_management': '',
        'rules': [],
        'coding_standards': [],
        'ui_guidelines': []
    }
    
    # Extract role of the agent
    role_match = re.search(r'You are (?:Z\.ai Code\. )?(.*?)\.', content[:200])
    if role_match:
        info['role'] = role_match.group(1)
    
    # Extract workflow steps (Important Rules section)
    workflow_match = re.search(r'# Important Rules(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if workflow_match:
        workflow_text = workflow_match.group(1)
        # Extract bullet points
        bullets = re.findall(r'-\s+(.*?)$', workflow_text, re.MULTILINE)
        info['workflow_steps'] = bullets
    
    # Extract technology stack information
    tech_stack_match = re.search(r'## Technology Stack Requirements(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if tech_stack_match:
        tech_stack_text = tech_stack_match.group(1)
        # Extract key technologies
        technologies = re.findall(r'-\s+\*\*(.*?)\*\*:?\s*(.*?)(?=\n|$)', tech_stack_text)
        info['tech_stack'] = technologies
    
    # Extract tools
    info['tools'] = extract_tools(file_path)
    
    # Extract rules
    rules_matches = re.findall(r'-\s+(.*?)$', content, re.MULTILINE)
    # Filter for rules that seem like imperative statements
    rules = [rule for rule in rules_matches if any(keyword in rule.lower() for keyword in ['must', 'always', 'never', 'do not', 'important'])]
    info['rules'] = rules[:10]  # Limit to first 10 rules
    
    # Extract coding standards
    coding_match = re.search(r'# Code Style(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if coding_match:
        coding_text = coding_match.group(1)
        coding_points = re.findall(r'-\s+(.*?)$', coding_text, re.MULTILINE)
        info['coding_standards'] = coding_points
    
    # Extract UI/UX guidelines
    ui_match = re.search(r'# UI/UX Design Standards(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if ui_match:
        ui_text = ui_match.group(1)
        ui_points = re.findall(r'-\s+\*\*(.*?)\*\*:?\s*(.*?)(?=\n|$)', ui_text)
        info['ui_guidelines'] = ui_points
    
    return info

def analyze_zai_prompt(file_path):
    """Main function to analyze the Z.ai prompt and generate structured data."""
    
    # Extract sections and count words
    sections, section_word_counts, total_words = extract_sections_and_count_words(file_path)
    
    # Count tools
    tool_count = count_tools(file_path)
    
    # Extract key information
    key_info = extract_key_info(file_path)
    
    # Prepare analysis data
    analysis_data = {
        'total_words': total_words,
        'tool_count': tool_count,
        'sections': section_word_counts,
        'key_info': key_info,
        'format': 'Plain Text'
    }
    
    return analysis_data

if __name__ == "__main__":
    file_path = "prompt.txt"
    
    # Analyze the prompt
    analysis_data = analyze_zai_prompt(file_path)
    
    # Save to JSON file for the visualization
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete!")
    print(f"Total words: {analysis_data['total_words']}")
    print(f"Number of tools: {analysis_data['tool_count']}")
    print(f"Format: {analysis_data['format']}")
    print("\nSections:")
    for section, count in analysis_data['sections'].items():
        print(f"  {section}: {count} words")
    print("\nTools found:")
    for tool in analysis_data['key_info']['tools']:
        print(f"  - {tool}")
import re
import json

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def count_words_in_json_like_text(file_path):
    """Count words in a JSON-like text file, focusing on text content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract all text content from the JSON-like text
    text_content = content
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', text_content)
    return len(words)

def extract_sections_and_content(file_path):
    """Extract sections from the system prompt text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on headers (lines starting with # or tags like <tag>)
    sections = {}
    current_section = "Introduction"
    current_text = ""
    
    for line in content.split('\n'):
        # Check for section headers (tags like <tag> or markdown-style headers)
        if line.strip().startswith('<') and '>' in line.strip() and not line.strip().startswith('</'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section (extract tag name)
            tag_match = re.match(r'<(\w+)', line.strip())
            if tag_match:
                current_section = tag_match.group(1).replace('_', ' ').title()
                current_text = ""
        elif line.strip().startswith('#'):
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
    
    return sections

def count_words_in_section(text):
    """Count words in a specific text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_section_word_counts(sections):
    """Count words in each section."""
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_text in sections.items():
        word_count = count_words_in_section(section_text)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    return section_word_counts, total_words

def extract_role_and_identity(content):
    """Extract role and identity information."""
    # Look for role/identity information
    role_patterns = [
        r'You are.*?(?:an AI|AI assistant|agent|assistant|engineer)',
        r'Role.*?:.*?(?:an AI|AI assistant|agent|assistant|engineer)',
        r'Identity.*?:.*?(?:an AI|AI assistant|agent|assistant|engineer)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return "Emergent AI Agent (E1)"

def extract_context_window(content):
    """Extract context window information if present."""
    # Look for context window information
    context_patterns = [
        r'context\s+window.*?(\d+)',
        r'context.*?limit.*?(\d+)',
        r'(\d+)\s+token.*?context',
        r'context.*?(\d+)\s+token'
    ]
    
    for pattern in context_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return f"{match.group(1)} tokens"
    
    return "Not specified"

def get_file_format(file_path):
    """Get the format of the file based on its extension."""
    if file_path.endswith('.txt'):
        return 'Plain Text'
    elif file_path.endswith('.json'):
        return 'JSON'
    else:
        return 'Unknown'

def extract_agentic_workflow(sections):
    """Extract information about the agentic workflow."""
    workflow_info = ""
    
    # Look for workflow-related sections
    workflow_keywords = ['workflow', 'approach', 'process', 'task', 'work', 'development']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in workflow_keywords):
            workflow_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return workflow_info.strip() if workflow_info else "Development workflow and processes defined"

def extract_rules(sections):
    """Extract rules and guidelines."""
    rules_info = ""
    
    # Look for rules-related sections
    rules_keywords = ['rule', 'guideline', 'principle', 'limitation', 'constraint', 'do', 'don\'t']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in rules_keywords):
            rules_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return rules_info.strip() if rules_info else "Rules and guidelines defined in multiple sections"

def extract_context_management(sections):
    """Extract context management information."""
    context_info = ""
    
    # Look for context-related sections
    context_keywords = ['context', 'environment', 'setup', 'variable', 'configuration']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in context_keywords):
            context_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return context_info.strip() if context_info else "Environment setup and context management defined"

def extract_coding_standards(sections):
    """Extract coding standards and best practices."""
    coding_info = ""
    
    # Look for coding-related sections
    coding_keywords = ['coding', 'code', 'programming', 'standard', 'practice', 'style', 'design']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in coding_keywords):
            coding_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return coding_info.strip() if coding_info else "Design guidelines and coding standards defined"

def extract_tools_info(file_path):
    """Extract information about tools from the Tools.json file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract tool names and descriptions
    tools_info = []
    
    # Find tool definitions in the JSON format
    tool_pattern = r'(\d+\.\s+)([a-zA-Z_]+)\s*\n\s*Description:\s*(.*?)(?=\n\d+\.|\Z)'
    matches = re.findall(tool_pattern, content, re.DOTALL)
    
    for match in matches:
        tool_name = match[1].strip()
        tool_description = match[2].strip()
        tools_info.append({
            'name': tool_name,
            'description': tool_description
        })
    
    return tools_info

if __name__ == "__main__":
    # File paths
    prompt_file = "Prompt.txt"
    tools_file = "Tools.json"
    
    # Count words in prompt file
    prompt_word_count = count_words_in_text(prompt_file)
    print(f"Words in prompt file: {prompt_word_count}")
    
    # Count words in tools file
    tools_word_count = count_words_in_json_like_text(tools_file)
    print(f"Words in tools file: {tools_word_count}")
    
    # Get file formats
    prompt_format = get_file_format(prompt_file)
    tools_format = get_file_format(tools_file)
    print(f"Prompt file format: {prompt_format}")
    print(f"Tools file format: {tools_format}")
    
    # Extract sections
    sections = extract_sections_and_content(prompt_file)
    print(f"\nNumber of sections in prompt: {len(sections)}")
    
    # Count words in each section
    section_word_counts, total_words = extract_section_word_counts(sections)
    print(f"Total words counted in sections: {total_words}")
    
    # Extract role information
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    role_info = extract_role_and_identity(content)
    print(f"Role information: {role_info}")
    
    # Extract context window
    context_window = extract_context_window(content)
    print(f"Context window: {context_window}")
    
    # Extract agentic workflow
    workflow_info = extract_agentic_workflow(sections)
    print(f"Workflow info extracted")
    
    # Extract rules
    rules_info = extract_rules(sections)
    print(f"Rules info extracted")
    
    # Extract context management
    context_info = extract_context_management(sections)
    print(f"Context management info extracted")
    
    # Extract coding standards
    coding_info = extract_coding_standards(sections)
    print(f"Coding standards info extracted")
    
    # Extract tools
    try:
        tools_info = extract_tools_info(tools_file)
        print(f"Extracted information for {len(tools_info)} tools")
    except Exception as e:
        print(f"Error extracting tools info: {e}")
        tools_info = []
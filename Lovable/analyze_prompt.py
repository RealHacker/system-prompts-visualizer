import re
import json

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def count_words_in_json(file_path):
    """Count words in a JSON file, focusing on text content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract all text content from the JSON
    text_content = ""
    
    def extract_text(obj):
        nonlocal text_content
        if isinstance(obj, dict):
            for value in obj.values():
                extract_text(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_text(item)
        elif isinstance(obj, str):
            text_content += obj + " "
    
    extract_text(data)
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', text_content)
    return len(words)

def count_tools_in_json(file_path):
    """Count the number of tools defined in the tools JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if isinstance(data, dict):
        return len(data)
    
    return 0

def extract_sections_and_content(file_path):
    """Extract sections from the system prompt text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on headers (lines starting with # or tags like <tag>)
    sections = {}
    current_section = "Introduction"
    current_text = ""
    
    for line in content.split('\n'):
        # Check for section headers (markdown-style headers)
        if line.strip().startswith('##'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section
            current_section = line.strip().strip('# ').strip()
            current_text = ""
        elif line.strip().startswith('#') and not line.strip().startswith('##'):
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

def extract_tool_info(file_path):
    """Extract information about each tool."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    tools_info = []
    if isinstance(data, dict):
        for tool_name, tool_data in data.items():
            if isinstance(tool_data, dict):
                tool_info = {
                    'name': tool_name,
                    'description': tool_data.get('description', 'No description provided')[:300] + '...' if len(tool_data.get('description', '')) > 300 else tool_data.get('description', 'No description provided')
                }
                tools_info.append(tool_info)
    
    return tools_info

def get_file_format(file_path):
    """Get the format of the file based on its extension."""
    if file_path.endswith('.txt'):
        return 'Plain Text'
    elif file_path.endswith('.json'):
        return 'JSON'
    else:
        return 'Unknown'

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

def extract_role_and_identity(content):
    """Extract role and identity information."""
    role_info = {}
    
    # Look for role/identity information
    role_patterns = [
        r'You are.*?(?:an AI|AI assistant|agent|assistant)',
        r'Role.*?:.*?(?:an AI|AI assistant|agent|assistant)',
        r'Identity.*?:.*?(?:an AI|AI assistant|agent|assistant)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            role_info['role'] = match.group(0)
            break
    
    return role_info

def extract_technology_stack(content):
    """Extract technology stack information."""
    tech_stack = []
    
    # Look for technology stack information
    tech_patterns = [
        r'Technology Stack:.*?([^\n]+)',
        r'Built on.*?([^\n]+)',
        r'Framework.*?:.*?([^\n]+)',
        r'Technologies.*?:.*?([^\n]+)'
    ]
    
    for pattern in tech_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            tech_stack.append(match.group(1).strip())
    
    return tech_stack

def extract_capabilities(content):
    """Extract capabilities information."""
    capabilities = []
    
    # Look for capabilities information
    capability_patterns = [
        r'Capabilities.*?:.*?([^\n]+)',
        r'Can.*?:.*?([^\n]+)',
        r'Able to.*?:.*?([^\n]+)'
    ]
    
    for pattern in capability_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        capabilities.extend(matches)
    
    return capabilities

if __name__ == "__main__":
    # File paths
    prompt_file = "Agent Prompt.txt"
    tools_file = "Agent Tools.json"
    
    # Count words in prompt file
    prompt_word_count = count_words_in_text(prompt_file)
    print(f"Words in prompt file: {prompt_word_count}")
    
    # Count words in tools file
    tools_word_count = count_words_in_json(tools_file)
    print(f"Words in tools file: {tools_word_count}")
    
    # Count tools
    tool_count = count_tools_in_json(tools_file)
    print(f"Number of tools: {tool_count}")
    
    # Get file formats
    prompt_format = get_file_format(prompt_file)
    tools_format = get_file_format(tools_file)
    print(f"Prompt file format: {prompt_format}")
    print(f"Tools file format: {tools_format}")
    
    # Extract sections
    sections = extract_sections_and_content(prompt_file)
    print(f"\nNumber of sections in prompt: {len(sections)}")
    
    # Extract tool information
    tools_info = extract_tool_info(tools_file)
    print(f"Extracted information for {len(tools_info)} tools")
    
    # Extract context window
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    context_window = extract_context_window(content)
    print(f"Context window: {context_window}")
    
    # Extract role information
    role_info = extract_role_and_identity(content)
    print(f"Role information: {role_info}")
    
    # Extract technology stack
    tech_stack = extract_technology_stack(content)
    print(f"Technology stack: {tech_stack}")
    
    # Extract capabilities
    capabilities = extract_capabilities(content)
    print(f"Capabilities: {capabilities}")
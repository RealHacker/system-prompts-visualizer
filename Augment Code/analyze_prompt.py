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
    
    if 'tools' in data:
        return len(data['tools'])
    
    return 0

def extract_sections_and_content(file_path):
    """Extract sections from the system prompt text file."""
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
    
    return sections

def extract_tool_info(file_path):
    """Extract information about each tool."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    tools_info = []
    if 'tools' in data and isinstance(data['tools'], list):
        for tool in data['tools']:
            if isinstance(tool, dict):
                tool_info = {
                    'name': tool.get('name', 'Unknown'),
                    'description': tool.get('description', 'No description provided')[:300] + '...' if len(tool.get('description', '')) > 300 else tool.get('description', 'No description provided')
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

if __name__ == "__main__":
    # File paths
    prompt_file = "claude-4-sonnet-agent-prompts.txt"
    tools_file = "claude-4-sonnet-tools.json"
    
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
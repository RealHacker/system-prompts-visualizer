import re
import yaml

def extract_sections_and_count_words(file_path):
    """Extract sections from the YAML system prompt and count words in each."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the YAML to extract text content
    try:
        data = yaml.safe_load(content)
        
        # Extract all text content from the system prompt
        text_content = ""
        if 'system' in data:
            for item in data['system']:
                if isinstance(item, dict) and 'text' in item:
                    text_content += item['text'] + "\n"
        
        # Extract sections based on headers (lines starting with #)
        sections = {}
        current_section = "Introduction"
        current_text = ""
        
        for line in text_content.split('\n'):
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
    
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}, {}, 0

def count_tools(file_path):
    """Count the number of tools defined in the YAML file."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    try:
        data = yaml.safe_load(content)
        
        if 'tools' in data and isinstance(data['tools'], list):
            return len(data['tools'])
        
        return 0
    
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return 0

def extract_tool_info(file_path):
    """Extract information about each tool."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    try:
        data = yaml.safe_load(content)
        
        tools_info = []
        if 'tools' in data and isinstance(data['tools'], list):
            for tool in data['tools']:
                if isinstance(tool, dict):
                    tool_info = {
                        'name': tool.get('name', 'Unknown'),
                        'description': tool.get('description', 'No description provided')[:200] + '...' if len(tool.get('description', '')) > 200 else tool.get('description', 'No description provided')
                    }
                    tools_info.append(tool_info)
        
        return tools_info
    
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return []

if __name__ == "__main__":
    file_path = "claude-4-sonnet.yaml"
    
    # Extract sections and count words
    sections, section_word_counts, total_words = extract_sections_and_count_words(file_path)
    
    # Count tools
    tool_count = count_tools(file_path)
    
    # Extract tool information
    tools_info = extract_tool_info(file_path)
    
    print(f"=== SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Number of tools: {tool_count}")
    print(f"Format: YAML")
    print()
    
    print("=== SECTION WORD COUNTS ===")
    for section, count in section_word_counts.items():
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        print(f"{section}: {count} words ({percentage:.1f}%)")
    
    print()
    print("=== TOOL INFORMATION ===")
    for tool in tools_info[:5]:  # Show first 5 tools
        print(f"Tool: {tool['name']}")
        print(f"Description: {tool['description']}")
        print()
    
    if len(tools_info) > 5:
        print(f"... and {len(tools_info) - 5} more tools")
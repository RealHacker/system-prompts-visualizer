import re
import json
import os

def extract_sections_and_count_words(prompt_file_path):
    """Extract sections from the system prompt and count words in each."""
    
    with open(prompt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on headers (lines starting with # or XML tags)
    sections = {}
    current_section = "Overview"
    current_text = ""
    
    for line in content.split('\n'):
        # Check for section headers (XML-like tags or markdown headers)
        if line.strip().startswith('<') and '>' in line.strip() and not line.strip().startswith('</'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section (remove < and >)
            tag = line.strip().split('>')[0].replace('<', '').strip()
            # Convert to title case and remove underscores
            current_section = ' '.join(word.capitalize() for word in tag.split('_'))
            current_text = ""
        elif line.strip().startswith('##') and not line.strip().startswith('###'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section (markdown header)
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

def count_tools(tools_file_path):
    """Count the number of tools defined in the JSON file."""
    
    if not os.path.exists(tools_file_path):
        return 0
    
    with open(tools_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    try:
        data = json.loads(content)
        
        # Count tools in the JSON structure
        if isinstance(data, dict):
            # If it's a dictionary of tools
            return len(data)
        elif isinstance(data, list):
            # If it's a list of tools
            return len(data)
        
        return 0
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return 0

def extract_tool_info(tools_file_path):
    """Extract information about each tool."""
    
    if not os.path.exists(tools_file_path):
        return []
    
    with open(tools_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    try:
        data = json.loads(content)
        
        tools_info = []
        if isinstance(data, dict):
            # Handle dictionary format
            for tool_name, tool_details in data.items():
                if isinstance(tool_details, dict):
                    tool_info = {
                        'name': tool_name,
                        'description': tool_details.get('description', 'No description provided')[:200] + '...' if len(tool_details.get('description', '')) > 200 else tool_details.get('description', 'No description provided')
                    }
                    tools_info.append(tool_info)
        elif isinstance(data, list):
            # Handle list format
            for tool in data:
                if isinstance(tool, dict):
                    tool_info = {
                        'name': tool.get('name', 'Unknown'),
                        'description': tool.get('description', 'No description provided')[:200] + '...' if len(tool.get('description', '')) > 200 else tool.get('description', 'No description provided')
                    }
                    tools_info.append(tool_info)
        
        return tools_info
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def analyze_trae_prompt():
    """Analyze the Trae prompt files and generate structured data."""
    
    prompt_file = "Builder Prompt.txt"
    tools_file = "Builder Tools.json"
    
    # Extract sections and count words
    sections, section_word_counts, total_words = extract_sections_and_count_words(prompt_file)
    
    # Count tools
    tool_count = count_tools(tools_file)
    
    # Extract tool information
    tools_info = extract_tool_info(tools_file)
    
    # Determine format
    format_type = "Plain Text with XML-like Tags"
    
    # Create analysis result
    analysis_result = {
        "total_words": total_words,
        "tool_count": tool_count,
        "format": format_type,
        "sections": section_word_counts,
        "tools": tools_info
    }
    
    # Save analysis result to JSON file
    with open("prompt_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, indent=2, ensure_ascii=False)
    
    print(f"=== TRAE SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Number of tools: {tool_count}")
    print(f"Format: {format_type}")
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

if __name__ == "__main__":
    analyze_trae_prompt()
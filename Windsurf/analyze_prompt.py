import re
import os

def count_words_in_text(text):
    """Count words in a text."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_sections_from_prompt(file_path):
    """Extract sections from the Windsurf prompt file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on XML-like tags
    sections = {}
    section_names = []
    
    # Find all tags
    tags = re.findall(r'<(\w+)>(.*?)</\1>', content, re.DOTALL)
    
    for tag, text in tags:
        section_name = tag.replace('_', ' ').title()
        sections[section_name] = text.strip()
        section_names.append(section_name)
    
    # Handle content outside tags as "Introduction"
    # Find content before first tag
    first_tag_match = re.search(r'<\w+>', content)
    if first_tag_match:
        intro_content = content[:first_tag_match.start()].strip()
        if intro_content:
            sections["Introduction"] = intro_content
            section_names.insert(0, "Introduction")
    
    # Count words in each section
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_text in sections.items():
        word_count = count_words_in_text(section_text)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    return sections, section_word_counts, total_words, section_names

def count_tools_in_tools_file(file_path):
    """Count the number of tools defined in the tools file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Count tools by looking for "type" declarations
    tool_matches = re.findall(r'type (\w+) =', content)
    return len(tool_matches)

def extract_tool_info(file_path):
    """Extract information about each tool."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract tool definitions
    tools_info = []
    tool_blocks = re.findall(r'type (\w+) = \(_: {(.*?)}\)(?: => any)?;', content, re.DOTALL)
    
    for tool_name, tool_content in tool_blocks:
        # Extract description (first line that looks like a comment)
        description_lines = [line.strip() for line in tool_content.split('\n') if line.strip().startswith('//')]
        description = " ".join([line[3:].strip() for line in description_lines[:2]]) if description_lines else "No description provided"
        
        # Extract parameters
        param_matches = re.findall(r'// (.*?): (.*?)\n', tool_content)
        params = [{"name": name.strip(), "description": desc.strip()} for desc, name in param_matches]
        
        tool_info = {
            'name': tool_name,
            'description': description,
            'parameters': params[:5]  # Limit to first 5 parameters
        }
        tools_info.append(tool_info)
    
    return tools_info

def analyze_windsurf_prompt():
    """Main function to analyze Windsurf prompt and tools."""
    prompt_file = "Prompt Wave 11.txt"
    tools_file = "Tools Wave 11.txt"
    
    # Extract sections and count words
    sections, section_word_counts, total_words, section_names = extract_sections_from_prompt(prompt_file)
    
    # Count tools
    tool_count = count_tools_in_tools_file(tools_file)
    
    # Extract tool information
    tools_info = extract_tool_info(tools_file)
    
    # Create analysis results
    analysis = {
        "total_words": total_words,
        "tool_count": tool_count,
        "format": "Plain text with XML-like tags",
        "sections": sections,
        "section_word_counts": section_word_counts,
        "section_names": section_names,
        "tools_info": tools_info
    }
    
    return analysis

if __name__ == "__main__":
    analysis = analyze_windsurf_prompt()
    
    print(f"=== WINDSURF SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {analysis['total_words']}")
    print(f"Number of tools: {analysis['tool_count']}")
    print(f"Format: {analysis['format']}")
    print()
    
    print("=== SECTION WORD COUNTS ===")
    for section in analysis['section_names']:
        count = analysis['section_word_counts'][section]
        percentage = (count / analysis['total_words']) * 100 if analysis['total_words'] > 0 else 0
        print(f"{section}: {count} words ({percentage:.1f}%)")
    
    print()
    print("=== TOOL INFORMATION ===")
    for tool in analysis['tools_info'][:5]:  # Show first 5 tools
        print(f"Tool: {tool['name']}")
        print(f"Description: {tool['description']}")
        if tool['parameters']:
            print("Parameters:")
            for param in tool['parameters'][:3]:  # Show first 3 parameters
                print(f"  - {param['name']}: {param['description']}")
        print()
    
    if len(analysis['tools_info']) > 5:
        print(f"... and {len(analysis['tools_info']) - 5} more tools")
import re
import os

def count_words(text):
    """Count words in text"""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_sections(content):
    """Extract sections from the prompt based on headers"""
    sections = {}
    
    # Split content into lines
    lines = content.split('\n')
    
    current_section = "Introduction"
    current_text = ""
    
    for line in lines:
        # Check if line is a header (starts with # or ##)
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

def count_tools(content):
    """Count the number of tools defined in the prompt"""
    # Look for tool definitions (## tool_name pattern)
    tool_pattern = r'##\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    tools = re.findall(tool_pattern, content)
    return len(tools)

def extract_tool_info(content):
    """Extract information about each tool"""
    tools_info = []
    
    # Split content by tool sections
    tool_sections = re.split(r'##\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
    
    # Process tool sections (skip first element which is text before first tool)
    for i in range(1, len(tool_sections), 2):
        if i + 1 < len(tool_sections):
            tool_name = tool_sections[i]
            tool_content = tool_sections[i + 1]
            
            # Extract description (first few lines after Description:)
            description_match = re.search(r'Description:\s*(.*?)(?=\n\n|\n[A-Z]|\Z)', tool_content, re.DOTALL)
            description = description_match.group(1).strip() if description_match else "No description provided"
            
            # Limit description length
            if len(description) > 200:
                description = description[:200] + "..."
            
            tools_info.append({
                'name': tool_name,
                'description': description
            })
    
    return tools_info

def analyze_prompt(file_path):
    """Main function to analyze the prompt file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections
    sections = extract_sections(content)
    
    # Count words in each section
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_text in sections.items():
        word_count = count_words(section_text)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    # Count tools
    tool_count = count_tools(content)
    
    # Extract tool information
    tools_info = extract_tool_info(content)
    
    return sections, section_word_counts, total_words, tool_count, tools_info

if __name__ == "__main__":
    file_path = "Prompt.txt"
    
    # Analyze the prompt
    sections, section_word_counts, total_words, tool_count, tools_info = analyze_prompt(file_path)
    
    print(f"=== SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Number of tools: {tool_count}")
    print(f"Format: Plain Text")
    print()
    
    print("=== SECTION WORD COUNTS ===")
    for section, count in section_word_counts.items():
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        print(f"{section}: {count} words ({percentage:.1f}%)")
    
    print()
    print("=== TOOL INFORMATION ===")
    for tool in tools_info[:10]:  # Show first 10 tools
        print(f"Tool: {tool['name']}")
        print(f"Description: {tool['description']}")
        print()
    
    if len(tools_info) > 10:
        print(f"... and {len(tools_info) - 10} more tools")
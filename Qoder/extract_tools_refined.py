import re
import json

def extract_tools_from_text(text):
    """Extract actual tool information from the system prompt text."""
    tools = []
    
    # Pattern to match the tools section in the prompt.txt file
    tools_section_pattern = r'## Available Tools[\s\S]*?(?=##|\Z)'
    tools_section_match = re.search(tools_section_pattern, text)
    
    if tools_section_match:
        tools_section = tools_section_match.group(0)
        
        # Extract individual tools with their descriptions
        # Pattern for tool names and descriptions in the format:
        # - **tool_name**: Description
        tool_pattern = r'- \*\*([A-Za-z_]\w*)\*\*:\s*([^\n\r]+)'
        tool_matches = re.finditer(tool_pattern, tools_section)
        
        for match in tool_matches:
            tool_name = match.group(1)
            tool_description = match.group(2).strip()
            tools.append({
                "name": tool_name,
                "description": tool_description
            })
    
    return tools

def extract_tools_from_file(file_path):
    """Extract tools from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return extract_tools_from_text(content)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def main():
    # Extract tools from the main prompt file where tools are defined
    tools = extract_tools_from_file("prompt.txt")
    
    # Save to JSON file
    with open("tools.json", "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=2)
    
    print(f"Total tools found: {len(tools)}")
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")

if __name__ == "__main__":
    main()
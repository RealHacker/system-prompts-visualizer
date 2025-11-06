import re
import json

def extract_tools_from_text(text):
    """Extract tool information from the system prompt text."""
    tools = []
    
    # Look for tool sections in the text
    # Pattern to match tool names and descriptions
    tool_pattern = r'(?:tool|function|method)[\s\-_]*(?:name|title)?:?\s*([A-Za-z_]\w*)[\s\S]*?(?:description|purpose):?\s*([^\n\r]+)'
    tool_matches = re.finditer(tool_pattern, text, re.IGNORECASE)
    
    for match in tool_matches:
        tool_name = match.group(1)
        tool_description = match.group(2).strip()
        tools.append({
            "name": tool_name,
            "description": tool_description
        })
    
    # Alternative pattern for tools in bullet points or lists
    tool_list_pattern = r'(?:\n|^)\s*[-*]\s*(?:tool:?\s*)?([A-Za-z_]\w*)[:\s]+([^\n\r]+)'
    tool_list_matches = re.finditer(tool_list_pattern, text, re.IGNORECASE)
    
    for match in tool_list_matches:
        tool_name = match.group(1)
        tool_description = match.group(2).strip()
        # Avoid duplicates
        if not any(tool["name"].lower() == tool_name.lower() for tool in tools):
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
    # Extract tools from each Qoder prompt file
    files = ["prompt.txt", "Quest Action.txt", "Quest Design.txt"]
    all_tools = []
    
    for file_name in files:
        file_path = f"{file_name}"
        tools = extract_tools_from_file(file_path)
        all_tools.extend(tools)
        print(f"Found {len(tools)} tools in {file_name}")
    
    # Remove duplicates based on tool name
    unique_tools = []
    seen_names = set()
    for tool in all_tools:
        if tool["name"].lower() not in seen_names:
            unique_tools.append(tool)
            seen_names.add(tool["name"].lower())
    
    # Save to JSON file
    with open("tools.json", "w", encoding="utf-8") as f:
        json.dump(unique_tools, f, indent=2)
    
    print(f"\nTotal unique tools found: {len(unique_tools)}")
    for tool in unique_tools:
        print(f"- {tool['name']}: {tool['description']}")

if __name__ == "__main__":
    main()
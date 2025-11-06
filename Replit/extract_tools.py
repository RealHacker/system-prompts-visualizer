import json

def extract_tools_info(tools_file_path):
    """Extract tools information from the tools JSON file."""
    with open(tools_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    tools = data.get('tools', [])
    return tools

def count_tools(tools_file_path):
    """Count the number of tools available."""
    tools = extract_tools_info(tools_file_path)
    return len(tools)

if __name__ == "__main__":
    tools = extract_tools_info("Tools.json")
    print(f"Total tools: {len(tools)}")
    for tool in tools[:5]:  # Print first 5 tools as examples
        print(f"- {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
import json

def extract_tool_details(file_path):
    """Extract detailed information about each tool."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    tools_details = []
    
    if isinstance(data, list):
        for i, tool in enumerate(data):
            if isinstance(tool, dict):
                tool_detail = {
                    'id': i,
                    'name': tool.get('name', 'Unknown'),
                    'description': tool.get('description', 'No description provided'),
                    'parameters': tool.get('parameters', {})
                }
                tools_details.append(tool_detail)
    
    return tools_details

def get_tool_names(file_path):
    """Get a list of tool names."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    tool_names = []
    
    if isinstance(data, list):
        for tool in data:
            if isinstance(tool, dict):
                tool_names.append(tool.get('name', 'Unknown'))
    
    return tool_names

def get_tool_count(file_path):
    """Get the number of tools."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if isinstance(data, list):
        return len(data)
    
    return 0

if __name__ == "__main__":
    tools_file = "Agent Tools v1.0.json"
    
    # Get tool count
    tool_count = get_tool_count(tools_file)
    print(f"Number of tools: {tool_count}")
    
    # Get tool names
    tool_names = get_tool_names(tools_file)
    print("Tool names:")
    for name in tool_names:
        print(f"  - {name}")
    
    # Get detailed tool information
    tools_details = extract_tool_details(tools_file)
    print("\nTool details:")
    for tool in tools_details:
        print(f"Name: {tool['name']}")
        print(f"Description: {tool['description'][:100]}...")
        print("---")
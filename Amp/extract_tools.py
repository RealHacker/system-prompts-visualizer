import yaml

def extract_all_tools(file_path):
    """Extract all tools with their full descriptions from the YAML file."""
    
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
                        'description': tool.get('description', 'No description provided')
                    }
                    tools_info.append(tool_info)
        
        return tools_info
    
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return []

if __name__ == "__main__":
    file_path = "claude-4-sonnet.yaml"
    
    # Extract tool information
    tools_info = extract_all_tools(file_path)
    
    print(f"Number of tools found: {len(tools_info)}")
    print("\n=== ALL TOOLS ===")
    for i, tool in enumerate(tools_info, 1):
        print(f"\n{i}. Tool: {tool['name']}")
        print(f"   Description: {tool['description']}")
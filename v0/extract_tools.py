import json
import re

def extract_tools_info(tools_data):
    """Extract and format tools information"""
    tools_list = []
    
    if 'tools' in tools_data:
        for tool in tools_data['tools']:
            # Extract parameters information
            parameters_info = []
            if 'parameters' in tool and 'properties' in tool['parameters']:
                props = tool['parameters']['properties']
                for param_name, param_details in props.items():
                    param_info = {
                        'name': param_name,
                        'type': param_details.get('type', 'unknown'),
                        'description': param_details.get('description', ''),
                        'required': param_name in tool['parameters'].get('required', [])
                    }
                    parameters_info.append(param_info)
            
            tool_info = {
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'parameters': parameters_info
            }
            tools_list.append(tool_info)
    
    return tools_list

def main():
    # Read tools file
    with open('Tools.json', 'r', encoding='utf-8') as f:
        tools_data = json.load(f)
    
    # Extract tools information
    tools_info = extract_tools_info(tools_data)
    
    # Save to JSON file
    with open('tools_extraction.json', 'w', encoding='utf-8') as f:
        json.dump(tools_info, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(tools_info)} tools")

if __name__ == '__main__':
    main()
import re
import json

def extract_tools_from_decision_prompt(file_path):
    """Extract tools information from the Decision-making prompt."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract tools section
    tools_match = re.search(r'<tools>\s*(.*?)\s*</tools>', content, re.DOTALL)
    if not tools_match:
        return []
    
    tools_content = tools_match.group(1)
    tools = []
    
    # Extract individual tools
    tool_lines = tools_content.strip().split('\n')
    for line in tool_lines:
        if line.strip().startswith('- '):
            tool_desc = line.strip()[2:]  # Remove "- " prefix
            if ':' in tool_desc:
                tool_name, tool_description = tool_desc.split(':', 1)
                tools.append({
                    'name': tool_name.strip(),
                    'description': tool_description.strip()
                })
    
    return tools

def extract_tools_from_system_prompt(file_path):
    """Extract tools information from the System Prompt."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    tools = []
    
    # Look for tools section in the format of function definitions
    tools_section = re.search(r'# Tools\s*\n\s*## functions\s*\n\s*namespace functions\s*{(.*?)}\s*// namespace functions', content, re.DOTALL)
    if tools_section:
        tools_content = tools_section.group(1)
        
        # Extract individual tool definitions
        tool_matches = re.findall(r'// (.*?)\s*type (\w+) = \(_:\s*//.*?{(.*?)}\s*\)', tools_content, re.DOTALL)
        for match in tool_matches:
            description, tool_name, params_content = match
            # Extract parameters
            params = []
            param_matches = re.findall(r'// (.*?)\s*//\s*\n\s*([\w_]+): ([^,}]+)', params_content, re.DOTALL)
            for param_match in param_matches:
                param_desc, param_name, param_type = param_match
                params.append({
                    'name': param_name.strip(),
                    'type': param_type.strip(),
                    'description': param_desc.strip()
                })
            
            tools.append({
                'name': tool_name,
                'description': description.strip(),
                'parameters': params
            })
    
    return tools

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_tools.py <prompt_type>")
        print("prompt_type: 'decision' or 'system'")
        sys.exit(1)
    
    prompt_type = sys.argv[1]
    
    if prompt_type == 'decision':
        tools = extract_tools_from_decision_prompt('Decision-making prompt.txt')
    elif prompt_type == 'system':
        tools = extract_tools_from_system_prompt('System Prompt.txt')
    else:
        print("Invalid prompt_type. Use 'decision' or 'system'")
        sys.exit(1)
    
    print(json.dumps(tools, indent=2))

if __name__ == "__main__":
    main()
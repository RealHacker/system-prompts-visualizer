#!/usr/bin/env python3
"""
Extract tools information from Codex CLI system prompts.
"""

import os
import json
import re

def read_file_content(file_path: str) -> str:
    """Read content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_tools_from_content(content: str) -> list:
    """Extract tool information from content."""
    tools = []
    
    # Pattern to match tool names in backticks
    tool_pattern = r'`(\w+)`'
    matches = re.finditer(tool_pattern, content)
    
    # Collect unique tool names
    tool_names = set()
    for match in matches:
        tool_name = match.group(1)
        if tool_name not in ['codex', 'help', 'git', 'rg', 'grep', 'cat']:
            tool_names.add(tool_name)
    
    # Extract detailed information for each tool
    for tool_name in tool_names:
        # Find all occurrences of the tool description
        tool_desc_pattern = rf'`{tool_name}`.*?(?=\n\n|\Z)'
        desc_matches = re.finditer(tool_desc_pattern, content, re.DOTALL)
        
        for desc_match in desc_matches:
            tool_desc = desc_match.group(0).strip()
            # Clean up the description
            tool_desc = re.sub(r'\s+', ' ', tool_desc)
            
            tools.append({
                'name': tool_name,
                'description': tool_desc
            })
    
    return tools

def main():
    """Main function to extract tools from Codex CLI prompts."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Process the main system prompt file
    prompt_file = os.path.join(script_dir, 'openai-codex-cli-system-prompt-20250820.txt')
    
    if os.path.exists(prompt_file):
        content = read_file_content(prompt_file)
        tools = extract_tools_from_content(content)
        
        # Save tools to JSON file
        tools_file = os.path.join(script_dir, 'tools.json')
        with open(tools_file, 'w', encoding='utf-8') as f:
            json.dump(tools, f, indent=2, ensure_ascii=False)
        
        print(f"Tools extracted: {len(tools)} tools found")
        print(f"Tools saved to {tools_file}")
        
        # Print tools summary
        for tool in tools:
            print(f"- {tool['name']}: {tool['description'][:100]}...")

if __name__ == '__main__':
    main()
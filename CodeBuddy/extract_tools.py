#!/usr/bin/env python3
"""
Extract detailed tool information from CodeBuddy system prompts.
"""

import re
import json
from typing import List, Dict, Any

def extract_tools_detailed(prompt_text: str) -> List[Dict[str, Any]]:
    """Extract detailed tool information."""
    tools = []
    
    # Pattern to match tool definitions
    # Look for ## tool_name pattern followed by description and details
    tool_sections = re.split(r'\n(##\s+[a-zA-Z_][a-zA-Z0-9_]*)\s*\n', prompt_text)
    
    # Process tool sections
    for i in range(1, len(tool_sections), 2):
        if i + 1 < len(tool_sections):
            tool_header = tool_sections[i]
            tool_content = tool_sections[i + 1]
            
            # Extract tool name
            tool_name_match = re.match(r'##\s+([a-zA-Z_][a-zA-Z0-9_]*)', tool_header)
            if tool_name_match:
                tool_name = tool_name_match.group(1)
                
                # Extract description (first paragraph after header)
                description_match = re.match(r'(.*?)(?:\n\n|\n====|\Z)', tool_content, re.DOTALL)
                description = description_match.group(1).strip() if description_match else ""
                
                # Extract parameters section
                parameters = []
                params_section = re.search(r'(Parameters?:.*?)(?=\n##|\n====|\Z)', tool_content, re.DOTALL)
                if params_section:
                    params_text = params_section.group(1)
                    # Find parameter lines
                    param_lines = re.findall(r'-\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*[:：]?\s*(.*?))?(?=\n-|\n##|\n====|\Z)', params_text, re.DOTALL)
                    for param_name, param_desc in param_lines:
                        parameters.append({
                            "name": param_name,
                            "description": param_desc.strip() if param_desc else ""
                        })
                
                # Extract usage example
                usage_match = re.search(r'Usage:\s*```.*?(<[^>]+>).*?```', tool_content, re.DOTALL)
                usage = usage_match.group(1) if usage_match else ""
                
                # Extract required parameters
                required_params = []
                required_match = re.search(r'Parameters?:\s*(?:\(|)(.*?)(?:\)|)(?=\s*(?:\n|$))', tool_content)
                if required_match:
                    required_text = required_match.group(1)
                    # Look for "required" indicators
                    required_items = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*[:：]?\s*\(required\)', required_text, re.IGNORECASE)
                    required_params = required_items
                
                tools.append({
                    "name": tool_name,
                    "description": description,
                    "parameters": parameters,
                    "required_parameters": required_params,
                    "usage_example": usage
                })
    
    return tools

def extract_modes_and_workflows(prompt_text: str) -> Dict[str, Any]:
    """Extract information about modes and workflows."""
    result = {
        "modes": [],
        "workflows": [],
        "rules": []
    }
    
    # Extract modes
    modes_pattern = r'##\s+(Main )?Mode\s*\n(.*?)(?=\n##|\n====|\Z)'
    modes_matches = re.finditer(modes_pattern, prompt_text, re.DOTALL)
    for match in modes_matches:
        mode_content = match.group(2)
        modes = re.findall(r'-\s+([A-Z\s]+):\s*(.*?)(?=\n-|\n##|\n====|\Z)', mode_content, re.DOTALL)
        for mode_name, mode_desc in modes:
            result["modes"].append({
                "name": mode_name.strip(),
                "description": mode_desc.strip()
            })
    
    # Extract workflows
    workflow_pattern = r'#\s+Tool Use Guidelines\s*\n(.*?)(?=\n##|\n====|\Z)'
    workflow_match = re.search(workflow_pattern, prompt_text, re.DOTALL)
    if workflow_match:
        workflow_text = workflow_match.group(1)
        steps = re.findall(r'\d+\.\s+(.*?)(?=\n\d+\.|\n##|\n====|\Z)', workflow_text, re.DOTALL)
        result["workflows"] = [step.strip() for step in steps]
    
    # Extract rules
    rules_pattern = r'====\s*\n\s*RULES\s*\n(.*?)(?=\n##|\n====|\Z)'
    rules_match = re.search(rules_pattern, prompt_text, re.DOTALL)
    if rules_match:
        rules_text = rules_match.group(1)
        rules = re.findall(r'-\s+(.*?)(?=\n-|\n##|\n====|\Z)', rules_text, re.DOTALL)
        result["rules"] = [rule.strip() for rule in rules]
    
    return result

def main():
    """Extract tools from both prompt files."""
    # Read both files
    with open("Chat Prompt.txt", "r", encoding="utf-8") as f:
        chat_content = f.read()
    
    with open("Craft Prompt.txt", "r", encoding="utf-8") as f:
        craft_content = f.read()
    
    # Extract tools
    chat_tools = extract_tools_detailed(chat_content)
    craft_tools = extract_tools_detailed(craft_content)
    
    # Extract modes and workflows
    chat_modes = extract_modes_and_workflows(chat_content)
    craft_modes = extract_modes_and_workflows(craft_content)
    
    # Prepare results
    results = {
        "chat_prompt": {
            "tools": chat_tools,
            "modes_and_workflows": chat_modes
        },
        "craft_prompt": {
            "tools": craft_tools,
            "modes_and_workflows": craft_modes
        }
    }
    
    # Save to file
    with open("tools_extraction.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("Tools extraction complete. Results saved to tools_extraction.json")
    print(f"Chat Prompt tools: {len(chat_tools)}")
    print(f"Craft Prompt tools: {len(craft_tools)}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Analyze CodeBuddy system prompts and extract structured information.
"""

import re
import json
from typing import Dict, List, Tuple, Any

def count_words(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

def extract_tools(prompt_text: str) -> List[Dict[str, Any]]:
    """Extract tool information from the prompt."""
    tools = []
    
    # Pattern to match tool sections
    tool_pattern = r'##\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\n(?:Description: (.*?)(?:\n|$))?(.*?)(?=\n## |\n====|\Z)'
    tool_matches = re.finditer(tool_pattern, prompt_text, re.DOTALL)
    
    for match in tool_matches:
        tool_name = match.group(1)
        description = match.group(2) if match.group(2) else ""
        details = match.group(3) if match.group(3) else ""
        
        # Extract parameters if available
        parameters = []
        param_pattern = r'-\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*[:：]?\s*(.*?))?(?=\n-|\n##|\n====|\Z)'
        param_matches = re.finditer(param_pattern, details, re.DOTALL)
        
        for param_match in param_matches:
            param_name = param_match.group(1)
            param_desc = param_match.group(2) if param_match.group(2) else ""
            parameters.append({
                "name": param_name,
                "description": param_desc.strip()
            })
        
        # Extract usage example if available
        usage_pattern = r'Usage:\s*```[^`]*<([^>]+)>[^`]*```'
        usage_match = re.search(usage_pattern, details, re.DOTALL)
        usage = usage_match.group(1) if usage_match else ""
        
        tools.append({
            "name": tool_name,
            "description": description.strip(),
            "parameters": parameters,
            "usage": usage
        })
    
    return tools

def extract_sections(prompt_text: str) -> Dict[str, str]:
    """Extract major sections from the prompt."""
    sections = {}
    
    # Split by major headers
    parts = re.split(r'\n(#+ .+?)\n', prompt_text)
    
    # First part is content before any header
    if parts and not re.match(r'^#+ .+', parts[0]):
        sections['introduction'] = parts[0].strip()
        parts = parts[1:]
    
    # Process pairs of headers and content
    for i in range(0, len(parts), 2):
        if i + 1 < len(parts):
            header = parts[i].strip()
            content = parts[i + 1].strip()
            
            # Normalize header to use as key
            header_key = re.sub(r'^#+\s*', '', header).lower()
            header_key = re.sub(r'[^a-z0-9\s]', '', header_key)
            header_key = re.sub(r'\s+', '_', header_key)
            
            sections[header_key] = content
    
    return sections

def analyze_prompt(file_path: str) -> Dict[str, Any]:
    """Analyze a prompt file and return structured information."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Basic statistics
    word_count = count_words(content)
    
    # Extract sections
    sections = extract_sections(content)
    
    # Extract tools
    tools = extract_tools(content)
    
    # Determine format
    format_type = "mixed"
    if re.search(r'<[a-zA-Z_][^>]*>', content):
        format_type = "xml"
    elif re.search(r'\{[a-zA-Z_][^}]*\}', content):
        format_type = "template"
    elif re.search(r'"[^"]*"\s*:', content):
        format_type = "json"
    
    return {
        "file_path": file_path,
        "word_count": word_count,
        "format": format_type,
        "sections": sections,
        "tools": tools,
        "total_tools": len(tools)
    }

def main():
    """Main function to analyze both prompt files."""
    chat_prompt_path = "Chat Prompt.txt"
    craft_prompt_path = "Craft Prompt.txt"
    
    # Analyze both prompts
    chat_analysis = analyze_prompt(chat_prompt_path)
    craft_analysis = analyze_prompt(craft_prompt_path)
    
    # Combine results
    result = {
        "chat_prompt": chat_analysis,
        "craft_prompt": craft_analysis
    }
    
    # Save to JSON file
    with open("prompt_analysis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("Analysis complete. Results saved to prompt_analysis.json")

if __name__ == "__main__":
    main()
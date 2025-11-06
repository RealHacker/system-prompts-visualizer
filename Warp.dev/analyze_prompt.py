#!/usr/bin/env python3
"""
Analyze the Warp.dev system prompt to extract tools and other structured information.
"""

import re
import json
from pathlib import Path

def extract_tools_info(prompt_text):
    """Extract tools information from the prompt."""
    tools_info = {}
    
    # Look for the tools section
    tools_section_match = re.search(r'# Tools\n(.*?)(?=\n# |\Z)', prompt_text, re.DOTALL)
    if tools_section_match:
        tools_section = tools_section_match.group(1)
        tools_info['section_content'] = tools_section.strip()
        
        # Extract individual tools
        tool_descriptions = re.findall(r'For the `(\w+)` tool:\n(.*?)(?=\nFor the|\Z)', tools_section, re.DOTALL)
        tools = {}
        for tool_name, description in tool_descriptions:
            tools[tool_name] = description.strip()
        
        tools_info['tools'] = tools
    
    return tools_info

def extract_rules(prompt_text):
    """Extract rules from the prompt."""
    rules = {}
    
    # Security rules
    security_rules = re.findall(r'IMPORTANT: (.+?)\.', prompt_text)
    rules['security'] = security_rules
    
    # Command execution rules
    cmd_rules_match = re.search(r'# Running terminal commands\n(.*?)(?=\n# |\Z)', prompt_text, re.DOTALL)
    if cmd_rules_match:
        cmd_rules = re.findall(r'IMPORTANT: (.+?)\.', cmd_rules_match.group(1))
        rules['command_execution'] = cmd_rules
    
    # File handling rules
    file_rules = []
    file_rules.extend(re.findall(r'IMPORTANT: Do not use terminal commands.*?\.', prompt_text))
    file_rules.extend(re.findall(r'IMPORTANT: NEVER edit files with terminal commands.*?\.', prompt_text))
    rules['file_handling'] = file_rules
    
    # Secret handling rules
    secret_rules_match = re.search(r'# Secrets and terminal commands\n(.*?)(?=\n# |\Z)', prompt_text, re.DOTALL)
    if secret_rules_match:
        secret_rules = re.findall(r'For any terminal commands.*?\.', secret_rules_match.group(1))
        rules['secret_handling'] = secret_rules
    
    return rules

def extract_workflow_info(prompt_text):
    """Extract workflow information."""
    workflow = {}
    
    # Question handling
    question_match = re.search(r'# Question\n(.*?)(?=\n# |\Z)', prompt_text, re.DOTALL)
    if question_match:
        workflow['question_handling'] = question_match.group(1).strip()
    
    # Task handling
    task_match = re.search(r'# Task\n(.*?)(?=\n# |\Z)', prompt_text, re.DOTALL)
    if task_match:
        task_content = task_match.group(1).strip()
        workflow['task_handling'] = task_content
        
        # Simple tasks
        simple_match = re.search(r'## Simple tasks\n(.*?)(?=\n## |\Z)', task_content, re.DOTALL)
        if simple_match:
            workflow['simple_tasks'] = simple_match.group(1).strip()
        
        # Complex tasks
        complex_match = re.search(r'## Complex tasks\n(.*?)(?=\n## |\Z)', task_content, re.DOTALL)
        if complex_match:
            workflow['complex_tasks'] = complex_match.group(1).strip()
    
    return workflow

def extract_coding_guidelines(prompt_text):
    """Extract coding guidelines."""
    coding = {}
    
    coding_match = re.search(r'# Coding\n(.*?)(?=\n# |\Z)', prompt_text, re.DOTALL)
    if coding_match:
        coding['guidelines'] = coding_match.group(1).strip()
    
    return coding

def main():
    # Read the prompt file
    prompt_path = Path("Prompt.txt")
    if not prompt_path.exists():
        print(f"Error: {prompt_path} not found")
        return
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_text = f.read()
    
    # Extract information
    analysis = {
        'tools': extract_tools_info(prompt_text),
        'rules': extract_rules(prompt_text),
        'workflow': extract_workflow_info(prompt_text),
        'coding': extract_coding_guidelines(prompt_text)
    }
    
    # Save to JSON file
    with open('prompt_analysis_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print("Detailed analysis saved to prompt_analysis_detailed.json")

if __name__ == "__main__":
    main()
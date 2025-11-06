#!/usr/bin/env python3
"""
Analyze the Junie system prompt and extract structured information.
"""

import re
import json
from typing import Dict, List, Any


def read_prompt_file(file_path: str) -> str:
    """Read the prompt file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def count_words(text: str) -> int:
    """Count the number of words in the text."""
    # Remove markdown formatting and count words
    clean_text = re.sub(r'[^\w\s]', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return len(clean_text.strip().split())


def extract_sections(prompt_text: str) -> Dict[str, Any]:
    """Extract major sections from the prompt."""
    sections = {}
    
    # Extract overview information
    overview_match = re.search(r'## ENVIRONMENT(.*?)## SPECIAL COMMANDS', prompt_text, re.DOTALL)
    if overview_match:
        overview_text = overview_match.group(1).strip()
        sections['overview'] = {
            'role': extract_role(overview_text),
            'format': 'markdown',
            'word_count': count_words(prompt_text),
            'context_window_limit': None  # Not specified in this prompt
        }
    
    # Extract special commands/tools
    tools_section_match = re.search(r'## SPECIAL COMMANDS(.*)', prompt_text, re.DOTALL)
    if tools_section_match:
        tools_text = tools_section_match.group(1)
        sections['tools'] = extract_tools(tools_text)
    
    # Extract workflow
    sections['workflow'] = extract_workflow(prompt_text)
    
    # Extract rules
    sections['rules'] = extract_rules(overview_text) if overview_match else []
    
    # Extract context management
    sections['context_management'] = extract_context_management(overview_text) if overview_match else {}
    
    return sections


def extract_role(overview_text: str) -> str:
    """Extract the role of the agent."""
    role_match = re.search(r"You're a helpful assistant designed to(.*?)(?:\.|$)", overview_text)
    if role_match:
        return "You're a helpful assistant designed to" + role_match.group(1) + "."
    return "Helpful assistant for exploring and clarifying user ideas, investigating project structures, and retrieving relevant code snippets."


def extract_workflow(prompt_text: str) -> List[str]:
    """Extract the agentic workflow."""
    workflow = [
        "1. Analyze user request to determine if project exploration is needed",
        "2. If general question, use `answer` command directly",
        "3. If project exploration needed, use special commands to investigate:",
        "   - Use `search_project` to find relevant code/files",
        "   - Use `get_file_structure` to understand file structure",
        "   - Use `open`/`open_entire_file` to view file contents",
        "   - Use `goto`/`scroll_up`/`scroll_down` to navigate files",
        "4. Compile findings and provide comprehensive answer using `answer` command"
    ]
    return workflow


def extract_rules(overview_text: str) -> List[str]:
    """Extract rules from the overview."""
    rules = []
    
    # Extract key rules
    if 'readonly mode' in overview_text.lower():
        rules.append("Work in readonly mode - don't modify, create or remove any files")
    
    if 'information from the `initial user context`' in overview_text.lower():
        rules.append("Use information from INITIAL USER CONTEXT block only when necessary for answering")
    
    if 'call `answer` command' in overview_text.lower():
        rules.append("When ready to give answer, call `answer` command with full answer")
        
    rules.extend([
        "Use special commands as listed in the prompt",
        "Use standard readonly bash commands (ls, cat, cd, etc.)",
        "No interactive commands (vim, python, etc.) are supported"
    ])
    
    return rules


def extract_context_management(overview_text: str) -> Dict[str, Any]:
    """Extract context management information."""
    return {
        "context_policy": "Use INITIAL USER CONTEXT block only when necessary",
        "eviction_policy": "Not explicitly specified",
        "memory_system": "Single-tier context system"
    }


def extract_tools(tools_text: str) -> List[Dict[str, Any]]:
    """Extract tools information."""
    tools = []
    
    # Pattern to match each tool section
    tool_pattern = r'### (\w+)\s*\n\*\*Signature\*\*:\s*\n`([^`]+)`\s*\n(?:#### Arguments\s*\n(.*?))?\s*\n#### Description\s*\n(.*?)(?=\s*#### Examples|\s*### |\s*$)'
    tool_matches = re.finditer(tool_pattern, tools_text, re.DOTALL)
    
    for match in tool_matches:
        tool_name = match.group(1)
        signature = match.group(2)
        arguments_text = match.group(3) if match.group(3) else ""
        description = match.group(4).strip()
        
        # Parse arguments
        arguments = []
        if arguments_text:
            arg_pattern = r'- \*\*(.*?)\*\* \(.*?\) \[(required|optional)\]: (.*)'
            arg_matches = re.finditer(arg_pattern, arguments_text)
            for arg_match in arg_matches:
                arguments.append({
                    "name": arg_match.group(1),
                    "required": arg_match.group(2) == "required",
                    "description": arg_match.group(3).strip()
                })
        
        # Extract examples if available
        examples = []
        examples_pattern = rf'#### Examples\s*\n(.*?)(?=\s*### |\s*$)'
        examples_match = re.search(examples_pattern, tools_text[match.start():], re.DOTALL)
        if examples_match:
            examples_text = examples_match.group(1)
            example_lines = [line.strip() for line in examples_text.strip().split('\n') if line.strip().startswith('-')]
            for line in example_lines:
                example = line.replace('- ', '').strip()
                examples.append(example)
        
        tools.append({
            "name": tool_name,
            "signature": signature,
            "description": description,
            "arguments": arguments,
            "examples": examples
        })
    
    return tools


def main():
    """Main function to analyze the prompt and save results."""
    prompt_path = 'Prompt.txt'
    output_path = 'prompt_analysis.json'
    
    # Read and analyze the prompt
    prompt_text = read_prompt_file(prompt_path)
    sections = extract_sections(prompt_text)
    
    # Count tools
    tool_count = len(sections.get('tools', []))
    if 'overview' in sections:
        sections['overview']['tool_count'] = tool_count
    
    # Save to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Results saved to {output_path}")
    return sections


if __name__ == '__main__':
    main()
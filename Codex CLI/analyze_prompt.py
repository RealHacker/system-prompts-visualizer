#!/usr/bin/env python3
"""
Analyze Codex CLI system prompts and extract structured information.
"""

import os
import re
import json
from typing import Dict, List, Tuple

def read_file_content(file_path: str) -> str:
    """Read content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())

def extract_sections(content: str) -> Dict[str, str]:
    """Extract major sections from the prompt."""
    sections = {}
    
    # Overview section
    overview_match = re.search(r'You are a coding agent.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if overview_match:
        sections['overview'] = overview_match.group(0).strip()
    
    # How you work section
    how_work_match = re.search(r'# How you work.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if how_work_match:
        sections['how_you_work'] = how_work_match.group(0).strip()
    
    # Personality section
    personality_match = re.search(r'## Personality.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if personality_match:
        sections['personality'] = personality_match.group(0).strip()
    
    # Planning section
    planning_match = re.search(r'## Planning.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if planning_match:
        sections['planning'] = planning_match.group(0).strip()
    
    # Task execution section
    task_exec_match = re.search(r'## Task execution.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if task_exec_match:
        sections['task_execution'] = task_exec_match.group(0).strip()
    
    # Testing section
    testing_match = re.search(r'## Testing your work.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if testing_match:
        sections['testing'] = testing_match.group(0).strip()
    
    # Sandbox section
    sandbox_match = re.search(r'## Sandbox and approvals.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if sandbox_match:
        sections['sandbox'] = sandbox_match.group(0).strip()
    
    # Ambition vs precision section
    ambition_match = re.search(r'## Ambition vs\. precision.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if ambition_match:
        sections['ambition_precision'] = ambition_match.group(0).strip()
    
    # Sharing progress section
    progress_match = re.search(r'## Sharing progress updates.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if progress_match:
        sections['progress_updates'] = progress_match.group(0).strip()
    
    # Presenting work section
    presenting_match = re.search(r'## Presenting your work and final message.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if presenting_match:
        sections['presenting_work'] = presenting_match.group(0).strip()
    
    # Tool guidelines section
    tool_guidelines_match = re.search(r'# Tool Guidelines.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if tool_guidelines_match:
        sections['tool_guidelines'] = tool_guidelines_match.group(0).strip()
    
    # Shell commands section
    shell_match = re.search(r'## Shell commands.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if shell_match:
        sections['shell_commands'] = shell_match.group(0).strip()
    
    # Apply patch section
    apply_patch_match = re.search(r'## `apply_patch`.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if apply_patch_match:
        sections['apply_patch'] = apply_patch_match.group(0).strip()
    
    # Update plan section
    update_plan_match = re.search(r'## `update_plan`.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if update_plan_match:
        sections['update_plan'] = update_plan_match.group(0).strip()
    
    return sections

def extract_tools(content: str) -> List[Dict[str, str]]:
    """Extract tool information from the prompt."""
    tools = []
    
    # Look for tool mentions in the content
    tool_patterns = [
        r'`apply_patch`.*?(?=\n\n|\Z)',
        r'`update_plan`.*?(?=\n\n|\Z)',
        r'`shell`.*?(?=\n\n|\Z)',
    ]
    
    for pattern in tool_patterns:
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            tool_desc = match.group(0).strip()
            # Extract tool name
            tool_name_match = re.search(r'`(\w+)`', tool_desc)
            if tool_name_match:
                tool_name = tool_name_match.group(1)
                tools.append({
                    'name': tool_name,
                    'description': tool_desc
                })
    
    return tools

def extract_rules(content: str) -> List[str]:
    """Extract rules from the prompt."""
    rules = []
    
    # Look for rule patterns
    rule_patterns = [
        r'- .*?(?=\n-|\n\n|\Z)',
        r'\*\*.*?\*\*:.*?(?=\n-|\n\n|\Z)',
    ]
    
    for pattern in rule_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            rule = match.group(0).strip()
            if rule.startswith('- ') or '**' in rule:
                rules.append(rule)
    
    return rules

def analyze_prompt(file_path: str) -> Dict:
    """Analyze a system prompt file and return structured data."""
    content = read_file_content(file_path)
    word_count = count_words(content)
    sections = extract_sections(content)
    tools = extract_tools(content)
    rules = extract_rules(content)
    
    # Calculate section word counts
    section_word_counts = {}
    for section_name, section_content in sections.items():
        section_word_counts[section_name] = count_words(section_content)
    
    return {
        'file_path': file_path,
        'total_word_count': word_count,
        'sections': sections,
        'section_word_counts': section_word_counts,
        'tools': tools,
        'rules': rules,
        'format': 'text'  # The format is plain text
    }

def main():
    """Main function to analyze Codex CLI prompts."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Analyze both prompt files
    prompt_files = [
        os.path.join(script_dir, 'Prompt.txt'),
        os.path.join(script_dir, 'openai-codex-cli-system-prompt-20250820.txt')
    ]
    
    analysis_results = {}
    for prompt_file in prompt_files:
        if os.path.exists(prompt_file):
            analysis_results[os.path.basename(prompt_file)] = analyze_prompt(prompt_file)
    
    # Save analysis results
    output_file = os.path.join(script_dir, 'prompt_analysis.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Results saved to {output_file}")

if __name__ == '__main__':
    main()
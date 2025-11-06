#!/usr/bin/env python3
"""
Count words in Codex CLI system prompt files and generate JSON output for visualization.
"""

import os
import json
import re

def count_words(text):
    """Count words in text."""
    return len(text.split())

def read_file(file_path):
    """Read file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_sections(content):
    """Analyze sections in the content and return word counts."""
    sections = {}
    
    # Overview section
    overview_match = re.search(r'You are a coding agent.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if overview_match:
        sections['Overview'] = count_words(overview_match.group(0))
    
    # How you work section
    how_work_match = re.search(r'# How you work.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if how_work_match:
        sections['How You Work'] = count_words(how_work_match.group(0))
    
    # Personality section
    personality_match = re.search(r'## Personality.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if personality_match:
        sections['Personality'] = count_words(personality_match.group(0))
    
    # Planning section
    planning_match = re.search(r'## Planning.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if planning_match:
        sections['Planning'] = count_words(planning_match.group(0))
    
    # Task execution section
    task_exec_match = re.search(r'## Task execution.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if task_exec_match:
        sections['Task Execution'] = count_words(task_exec_match.group(0))
    
    # Testing section
    testing_match = re.search(r'## Testing your work.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if testing_match:
        sections['Testing'] = count_words(testing_match.group(0))
    
    # Sandbox section
    sandbox_match = re.search(r'## Sandbox and approvals.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if sandbox_match:
        sections['Sandbox & Approvals'] = count_words(sandbox_match.group(0))
    
    # Ambition vs precision section
    ambition_match = re.search(r'## Ambition vs\. precision.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if ambition_match:
        sections['Ambition vs Precision'] = count_words(ambition_match.group(0))
    
    # Sharing progress section
    progress_match = re.search(r'## Sharing progress updates.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if progress_match:
        sections['Progress Updates'] = count_words(progress_match.group(0))
    
    # Presenting work section
    presenting_match = re.search(r'## Presenting your work and final message.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if presenting_match:
        sections['Presenting Work'] = count_words(presenting_match.group(0))
    
    # Tool guidelines section
    tool_guidelines_match = re.search(r'# Tool Guidelines.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if tool_guidelines_match:
        sections['Tool Guidelines'] = count_words(tool_guidelines_match.group(0))
    
    # Shell commands section
    shell_match = re.search(r'## Shell commands.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if shell_match:
        sections['Shell Commands'] = count_words(shell_match.group(0))
    
    # Apply patch section
    apply_patch_match = re.search(r'## `apply_patch`.*?(?=\n#{2,3}|\Z)', content, re.DOTALL)
    if apply_patch_match:
        sections['Apply Patch'] = count_words(apply_patch_match.group(0))
    
    # Update plan section
    update_plan_match = re.search(r'## `update_plan`.*?(?=\n#{1,2}|\Z)', content, re.DOTALL)
    if update_plan_match:
        sections['Update Plan'] = count_words(update_plan_match.group(0))
    
    return sections

def main():
    """Main function to count words and generate JSON output."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Process both prompt files
    files_to_process = [
        ('Prompt.txt', 'Prompt.txt'),
        ('openai-codex-cli-system-prompt-20250820.txt', 'System Prompt 2025-08-20')
    ]
    
    all_word_counts = {}
    
    for file_name, display_name in files_to_process:
        file_path = os.path.join(script_dir, file_name)
        if os.path.exists(file_path):
            content = read_file(file_path)
            total_words = count_words(content)
            section_counts = analyze_sections(content)
            
            all_word_counts[display_name] = {
                'total_words': total_words,
                'sections': section_counts
            }
    
    # Save to JSON file
    output_file = os.path.join(script_dir, 'word_count.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_word_counts, f, indent=2, ensure_ascii=False)
    
    print(f"Word count analysis complete. Results saved to {output_file}")

if __name__ == '__main__':
    main()
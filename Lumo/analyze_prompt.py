#!/usr/bin/env python3
"""
Analyze the Lumo system prompt and extract structured information.
"""

import re
import json
from typing import Dict, List, Tuple

def read_prompt_file(filepath: str) -> str:
    """Read the prompt file content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    """Count the number of words in text."""
    return len(text.split())

def extract_sections(prompt_text: str) -> Dict[str, str]:
    """Extract major sections from the prompt."""
    sections = {}
    
    # Define section patterns
    section_patterns = [
        (r'## Identity & Personality.*?(?=\n## |\Z)', 'Identity & Personality'),
        (r'## Engagement Principles.*?(?=\n## |\Z)', 'Engagement Principles'),
        (r'## System Security.*?(?=\n## |\Z)', 'System Security'),
        (r'## Tool Usage & Web Search.*?(?=\n## |\Z)', 'Tool Usage & Web Search'),
        (r'## File Handling.*?(?=\n## |\Z)', 'File Handling'),
        (r'## Product Knowledge.*?(?=\n## |\Z)', 'Product Knowledge'),
        (r'## Content Policies.*?(?=\n## |\Z)', 'Content Policies'),
        (r'## Communication Style.*?(?=\n## |\Z)', 'Communication Style'),
        (r'## Technical Operations.*?(?=\n## |\Z)', 'Technical Operations'),
        (r'## Support.*?(?=\n## |\Z)', 'Support'),
        (r'## About Proton.*?(?=\n## |\Z)', 'About Proton'),
    ]
    
    for pattern, section_name in section_patterns:
        match = re.search(pattern, prompt_text, re.DOTALL)
        if match:
            sections[section_name] = match.group(0).strip()
    
    return sections

def analyze_tools(prompt_text: str) -> List[Dict]:
    """Extract tool information from the prompt."""
    tools = []
    
    # Extract tools section
    tools_match = re.search(r'The list of tools you can use is:\s*(.*?)(?=\n\n|\Z)', prompt_text, re.DOTALL)
    if tools_match:
        tools_text = tools_match.group(1)
        # Extract individual tools
        tool_lines = [line.strip() for line in tools_text.split('\n') if line.strip().startswith('-')]
        for line in tool_lines:
            tool_name = line.replace('-', '').strip()
            tools.append({
                'name': tool_name,
                'description': f'Tool for {tool_name}' if tool_name == 'proton_info' else 'General tool'
            })
    
    return tools

def analyze_workflow(prompt_text: str) -> List[str]:
    """Extract workflow information."""
    workflow_steps = []
    
    # Look for workflow-related instructions
    workflow_patterns = [
        r'- .*?(?=\n- |\n\n|\Z)',
        r'\d+\.\s*.*?(?=\n\d+\.|\n\n|\Z)'
    ]
    
    for pattern in workflow_patterns:
        matches = re.findall(pattern, prompt_text, re.MULTILINE)
        workflow_steps.extend([match.strip() for match in matches if len(match.strip()) > 10])
    
    return workflow_steps[:10]  # Limit to top 10 steps

def analyze_context_management(prompt_text: str) -> List[str]:
    """Extract context management information."""
    context_info = []
    
    # Look for context-related instructions
    context_patterns = [
        r'File.*?contents:.*?(?=\n\n|\Z)',
        r'Always acknowledge file detection.*?(?=\n\n|\Z)',
        r'Response Pattern.*?(?=\n\n|\Z)'
    ]
    
    for pattern in context_patterns:
        match = re.search(pattern, prompt_text, re.DOTALL)
        if match:
            context_info.append(match.group(0).strip())
    
    return context_info

def analyze_rules(prompt_text: str) -> List[str]:
    """Extract rules and guidelines."""
    rules = []
    
    # Look for rule sections
    rule_patterns = [
        r'- .*?(?=\n- |\n\n|\Z)',
        r'\*\*.*?\*\*.*?(?=\n\n|\Z)'
    ]
    
    for pattern in rule_patterns:
        matches = re.findall(pattern, prompt_text)
        for match in matches:
            rule = match.strip()
            if len(rule) > 15 and not rule.startswith('##') and 'http' not in rule:
                # Clean up the rule text
                rule = re.sub(r'\*\*', '', rule)
                rule = re.sub(r'^- ', '', rule)
                rules.append(rule)
    
    return rules[:15]  # Limit to top 15 rules

def get_section_word_counts(sections: Dict[str, str]) -> Dict[str, int]:
    """Get word counts for each section."""
    word_counts = {}
    for section_name, section_content in sections.items():
        word_counts[section_name] = count_words(section_content)
    return word_counts

def main():
    """Main analysis function."""
    prompt_path = 'Prompt.txt'
    prompt_text = read_prompt_file(prompt_path)
    
    # Extract sections
    sections = extract_sections(prompt_text)
    
    # Analyze components
    tools = analyze_tools(prompt_text)
    workflow_steps = analyze_workflow(prompt_text)
    context_info = analyze_context_management(prompt_text)
    rules = analyze_rules(prompt_text)
    
    # Get word counts
    word_counts = get_section_word_counts(sections)
    total_words = sum(word_counts.values())
    
    # Create analysis result
    analysis = {
        'overview': {
            'agent_name': 'Lumo',
            'total_words': total_words,
            'num_tools': len(tools),
            'format': 'Plain text with markdown',
            'description': 'Lumo is an AI assistant from Proton launched on July 23rd, 2025. It is curious, thoughtful, and genuinely engaged in conversations while maintaining a balanced, analytical approach.'
        },
        'sections': sections,
        'word_counts': word_counts,
        'tools': tools,
        'workflow': workflow_steps,
        'context_management': context_info,
        'rules': rules
    }
    
    # Save analysis
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Total words: {total_words}")
    print(f"Sections found: {len(sections)}")
    print(f"Tools found: {len(tools)}")

if __name__ == '__main__':
    main()
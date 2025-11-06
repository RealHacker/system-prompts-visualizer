#!/usr/bin/env python3
"""
Count words in the Lumo prompt and generate visualization data.
"""

import json
import re

def read_prompt_file(filepath: str) -> str:
    """Read the prompt file content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    """Count the number of words in text."""
    return len(text.split())

def get_section_word_counts(prompt_text: str) -> dict:
    """Get word counts for major sections."""
    sections = {}
    
    # Define section patterns with their display names
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
    
    total_words = count_words(prompt_text)
    
    for pattern, section_name in section_patterns:
        match = re.search(pattern, prompt_text, re.DOTALL)
        if match:
            section_content = match.group(0).strip()
            word_count = count_words(section_content)
            percentage = round((word_count / total_words) * 100, 1) if total_words > 0 else 0
            sections[section_name] = {
                'words': word_count,
                'percentage': percentage
            }
    
    return sections, total_words

def main():
    """Main function to generate word count data."""
    prompt_text = read_prompt_file('Prompt.txt')
    section_data, total_words = get_section_word_counts(prompt_text)
    
    # Convert to format suitable for visualization
    visualization_data = []
    colors = [
        '#4361ee', '#3f37c9', '#4895ef', '#4cc9f0', '#f72585',
        '#e63946', '#7209b7', '#560bad', '#3a0ca3', '#4cc9f0',
        '#f72585'
    ]
    
    for i, (section_name, data) in enumerate(section_data.items()):
        color_index = i % len(colors)
        visualization_data.append({
            'name': section_name,
            'words': data['words'],
            'percentage': data['percentage'],
            'color': colors[color_index]
        })
    
    # Save word count data
    word_count_data = {
        'total_words': total_words,
        'sections': visualization_data
    }
    
    with open('word_count.json', 'w', encoding='utf-8') as f:
        json.dump(word_count_data, f, indent=2)
    
    print(f"Word count analysis complete. Total words: {total_words}")

if __name__ == '__main__':
    main()
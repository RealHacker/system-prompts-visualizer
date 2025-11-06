#!/usr/bin/env python3

import sys
import re
from collections import defaultdict

def count_words_in_section(section_content):
    """Count words in a section of text."""
    # Remove extra whitespace and count words
    words = re.findall(r'\b\w+\b', section_content)
    return len(words)

def analyze_prompt_sections(file_path):
    """Analyze the Bolt prompt and count words in each section."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define sections based on XML tags
    sections = {
        'Overview': 'Overall role and description',
        'System Constraints': '<system_constraints>',
        'Database Instructions': '<database_instructions>',
        'Code Formatting': '<code_formatting_info>',
        'Message Formatting': '<message_formatting_info>',
        'Chain of Thought': '<chain_of_thought_instructions>',
        'Artifact Info': '<artifact_info>',
        'Examples': '<examples>'
    }
    
    section_word_counts = {}
    section_contents = {}
    
    # Extract and count each section
    for section_name, tag in sections.items():
        if tag.startswith('<'):
            # XML tag section
            start_tag = tag
            end_tag = tag.replace('<', '</')
            match = re.search(f'{re.escape(start_tag)}(.*?){re.escape(end_tag)}', content, re.DOTALL)
            if match:
                section_content = match.group(1)
                section_contents[section_name] = section_content.strip()
                section_word_counts[section_name] = count_words_in_section(section_content)
            else:
                section_contents[section_name] = ""
                section_word_counts[section_name] = 0
        else:
            # Special handling for overview (first part of the document)
            if section_name == 'Overview':
                # Get content up to the first XML tag
                first_tag_match = re.search(r'<\w+_', content)
                if first_tag_match:
                    overview_content = content[:first_tag_match.start()]
                    section_contents[section_name] = overview_content.strip()
                    section_word_counts[section_name] = count_words_in_section(overview_content)
                else:
                    section_contents[section_name] = content[:1000]  # First 1000 chars as fallback
                    section_word_counts[section_name] = count_words_in_section(section_contents[section_name])
    
    # Calculate total words
    total_words = len(re.findall(r'\b\w+\b', content))
    
    return section_word_counts, section_contents, total_words

def main():
    """Main function to analyze word counts."""
    if len(sys.argv) != 2:
        print("Usage: python word_count.py <prompt_file>")
        sys.exit(1)
    
    prompt_file = sys.argv[1]
    word_counts, contents, total_words = analyze_prompt_sections(prompt_file)
    
    # Print results
    print(f"Total words in prompt: {total_words}")
    print("\nWord count by section:")
    print("-" * 30)
    
    for section, count in word_counts.items():
        print(f"{section:<25}: {count:>5} words")
    
    # Save to JSON file for visualization
    import json
    result = {
        'total_words': total_words,
        'section_word_counts': word_counts,
        'sections': list(word_counts.keys())
    }
    
    with open('word_count.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nDetailed results saved to word_count.json")

if __name__ == "__main__":
    main()
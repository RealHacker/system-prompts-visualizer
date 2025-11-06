#!/usr/bin/env python3
"""
Word count utility for the Junie system prompt.
"""

import re
import json


def count_words(text):
    """Count words in text."""
    # Clean up the text
    clean_text = re.sub(r'[^\w\s]', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    words = clean_text.strip().split()
    return len(words)


def count_characters(text):
    """Count characters in text."""
    return len(text)


def count_lines(text):
    """Count lines in text."""
    return len(text.splitlines())


def analyze_prompt_complexity(text):
    """Analyze complexity of the prompt."""
    # Count sections
    sections = re.findall(r'##+ .+', text)
    section_count = len(sections)
    
    # Count code blocks
    code_blocks = re.findall(r'`[^`]+`', text)
    code_block_count = len(code_blocks)
    
    # Count lists
    lists = re.findall(r'^\s*[-*]\s+|^\s*\d+\.\s+', text, re.MULTILINE)
    list_count = len(lists)
    
    return {
        'section_count': section_count,
        'code_block_count': code_block_count,
        'list_count': list_count
    }


def main():
    """Main function to count words in the prompt."""
    # Read the prompt file
    with open('Prompt.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get counts
    word_count = count_words(content)
    char_count = count_characters(content)
    line_count = count_lines(content)
    complexity = analyze_prompt_complexity(content)
    
    # Create results dictionary
    results = {
        'word_count': word_count,
        'character_count': char_count,
        'line_count': line_count,
        'complexity_metrics': complexity
    }
    
    # Save to file
    with open('word_count.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Print results
    print(f"Word count: {word_count}")
    print(f"Character count: {char_count}")
    print(f"Line count: {line_count}")
    print(f"Sections: {complexity['section_count']}")
    print(f"Code blocks: {complexity['code_block_count']}")
    print(f"List items: {complexity['list_count']}")


if __name__ == '__main__':
    main()
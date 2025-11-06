#!/usr/bin/env python3
"""
Count words in GitHub Copilot prompt files and generate statistics.
"""

import os
import json

def read_file(file_path: str) -> str:
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

def count_lines(text: str) -> int:
    """Count the number of lines in a text."""
    return len(text.splitlines())

def analyze_files():
    """Analyze GitHub Copilot prompt files."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Files to analyze
    files = ['Prompt.txt', 'gpt-5.txt']
    
    # Results
    results = {
        'files': {},
        'total': {
            'words': 0,
            'lines': 0
        }
    }
    
    # Analyze each file
    for filename in files:
        file_path = os.path.join(script_dir, filename)
        if os.path.exists(file_path):
            content = read_file(file_path)
            word_count = count_words(content)
            line_count = count_lines(content)
            
            results['files'][filename] = {
                'words': word_count,
                'lines': line_count
            }
            
            results['total']['words'] += word_count
            results['total']['lines'] += line_count
    
    # Save results
    output_file = os.path.join(script_dir, 'word_count.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Print results
    print("GitHub Copilot Prompt Analysis")
    print("=" * 40)
    for filename, stats in results['files'].items():
        print(f"{filename}:")
        print(f"  Words: {stats['words']:,}")
        print(f"  Lines: {stats['lines']:,}")
        print()
    
    print(f"Total:")
    print(f"  Words: {results['total']['words']:,}")
    print(f"  Lines: {results['total']['lines']:,}")
    
    return results

if __name__ == '__main__':
    analyze_files()
#!/usr/bin/env python3
"""
Analyze word count and section distribution of the Warp.dev system prompt.
"""

import re
import json
from pathlib import Path

def count_words(text):
    """Count words in text."""
    return len(re.findall(r'\b\w+\b', text))

def analyze_prompt_sections(prompt_text):
    """Analyze sections in the prompt."""
    sections = {}
    
    # Find all main sections (lines starting with #)
    section_pattern = r'^# (.+)$'
    lines = prompt_text.split('\n')
    
    current_section = None
    section_content = []
    
    for line in lines:
        # Check if this is a section header
        if line.startswith('# ') and not line.startswith('##'):
            # Save previous section if exists
            if current_section:
                sections[current_section] = '\n'.join(section_content)
            
            # Start new section
            current_section = line[2:].strip()
            section_content = []
        elif current_section:
            section_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(section_content)
    
    # Also handle subsections (##)
    subsections = {}
    current_main_section = None
    
    for line in lines:
        if line.startswith('# ') and not line.startswith('##'):
            current_main_section = line[2:].strip()
        elif line.startswith('## ') and current_main_section:
            subsection_title = line[3:].strip()
            subsections[subsection_title] = current_main_section
    
    return sections, subsections

def main():
    # Read the prompt file
    prompt_path = Path("Prompt.txt")
    if not prompt_path.exists():
        print(f"Error: {prompt_path} not found")
        return
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_text = f.read()
    
    # Basic statistics
    total_words = count_words(prompt_text)
    
    # Analyze sections
    sections, subsections = analyze_prompt_sections(prompt_text)
    
    # Count words in each section
    section_word_counts = {}
    for section_name, section_content in sections.items():
        section_word_counts[section_name] = count_words(section_content)
    
    # Prepare analysis data
    analysis_data = {
        "total_words": total_words,
        "sections": section_word_counts,
        "subsections": subsections
    }
    
    # Save to JSON file
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"Total words: {total_words}")
    print("\nSection word counts:")
    for section, count in section_word_counts.items():
        print(f"  {section}: {count}")
    
    print(f"\nSections: {len(sections)}")
    print(f"Subsections: {len(subsections)}")

if __name__ == "__main__":
    main()
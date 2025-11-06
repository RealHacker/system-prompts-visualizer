import re

def count_words_in_section(text):
    """Count words in a text section"""
    # Remove extra whitespace and count words
    return len(text.strip().split())

def extract_and_count_sections(prompt_file):
    """Extract sections from prompt file and count words"""
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define section patterns based on the actual Same.dev prompt structure
    sections = {
        'Overview': r'Knowledge cutoff:.*?(?=<.*?>|\Z)',
        'Service Policies': r'<service_policies>(.*?)</service_policies>',
        'Communication': r'<communication>(.*?)</communication>',
        'Tool Calling': r'<tool_calling>(.*?)</tool_calling>',
        'Parallel Tool Calls': r'<maximize_parallel_tool_calls>(.*?)</maximize_parallel_tool_calls>',
        'Memos': r'<memos>(.*?)</memos>',
        'Making Code Changes': r'<making_code_changes>(.*?)</making_code_changes>',
        'Web Development': r'<web_development>(.*?)</web_development>',
        'Web Design': r'<web_design>(.*?)</web_design>',
        'Debugging': r'<debugging>(.*?)</debugging>',
        'Website Cloning': r'<website_cloning>(.*?)</website_cloning>',
        'Task Agent': r'<task_agent>(.*?)</task_agent>'
    }
    
    section_word_counts = {}
    total_words = 0
    
    # Handle overview section separately (not in tags)
    overview_match = re.search(r'Knowledge cutoff:.*?(?=<.*?>|\Z)', content, re.DOTALL)
    if overview_match:
        overview_text = overview_match.group(0)
        overview_count = count_words_in_section(overview_text)
        section_word_counts['Overview'] = overview_count
        total_words += overview_count
    
    # Handle tagged sections
    for section_name, pattern in sections.items():
        if section_name == 'Overview':
            continue  # Already handled
        match = re.search(pattern, content, re.DOTALL)
        if match:
            section_text = match.group(1)
            word_count = count_words_in_section(section_text)
            section_word_counts[section_name] = word_count
            total_words += word_count
    
    return section_word_counts, total_words

if __name__ == "__main__":
    section_counts, total = extract_and_count_sections('Prompt.txt')
    
    print("Section Word Counts:")
    print("-" * 30)
    for section, count in section_counts.items():
        print(f"{section}: {count} words")
    
    print("-" * 30)
    print(f"Total words in prompt: {total}")
    
    # Save to a file for the visualization
    with open('word_count.json', 'w') as f:
        import json
        json.dump({
            'section_counts': section_counts,
            'total_words': total
        }, f, indent=2)
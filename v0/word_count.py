import re
import json

def count_words_in_text(text):
    """Count words in text, excluding code blocks"""
    # Remove code blocks
    text_without_code = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text_without_code = re.sub(r'`[^`]*`', '', text_without_code)
    # Count words
    words = re.findall(r'\b\w+\b', text_without_code)
    return len(words)

def count_words_in_file(filepath):
    """Count words in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return count_words_in_text(content)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

def count_words_in_section(content, section_name):
    """Count words in a specific section"""
    return count_words_in_text(content)

def main():
    # Count words in prompt file
    prompt_words = count_words_in_file('Prompt.txt')
    
    # Count words in tools file (as text)
    tools_words = count_words_in_file('Tools.json')
    
    # Create word count results
    word_counts = {
        'Prompt.txt': prompt_words,
        'Tools.json': tools_words,
        'total': prompt_words + tools_words
    }
    
    # Save to JSON file
    with open('word_count.json', 'w') as f:
        json.dump(word_counts, f, indent=2)
    
    print(f"Word count results:")
    print(f"Prompt.txt: {prompt_words} words")
    print(f"Tools.json: {tools_words} words")
    print(f"Total: {word_counts['total']} words")

if __name__ == '__main__':
    main()
import re
import json

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def count_words_in_json(file_path):
    """Count words in a JSON file, focusing on text content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract all text content from the JSON
    text_content = ""
    
    def extract_text(obj):
        nonlocal text_content
        if isinstance(obj, dict):
            for value in obj.values():
                extract_text(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_text(item)
        elif isinstance(obj, str):
            text_content += obj + " "
    
    extract_text(data)
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', text_content)
    return len(words)

def count_words_in_section(text):
    """Count words in a text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

if __name__ == "__main__":
    # Example usage
    prompt_file = "claude-code-system-prompt.txt"
    tools_file = "claude-code-tools.json"
    
    prompt_word_count = count_words_in_text(prompt_file)
    tools_word_count = count_words_in_json(tools_file)
    
    print(f"Prompt word count: {prompt_word_count}")
    print(f"Tools word count: {tools_word_count}")
    print(f"Total word count: {prompt_word_count + tools_word_count}")
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

if __name__ == "__main__":
    prompt_file = "Agent Prompt.txt"
    tools_file = "Agent Tools.json"
    
    # Count words in prompt file
    prompt_word_count = count_words_in_text(prompt_file)
    print(f"Words in prompt file: {prompt_word_count}")
    
    # Count words in tools file
    tools_word_count = count_words_in_json(tools_file)
    print(f"Words in tools file: {tools_word_count}")
    
    # Total word count
    total_words = prompt_word_count + tools_word_count
    print(f"Total words in system prompt and tools: {total_words}")
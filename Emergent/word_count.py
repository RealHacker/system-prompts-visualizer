import re

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def count_words_in_json_like_text(file_path):
    """Count words in a JSON-like text file, focusing on text content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract all text content from the JSON-like text
    text_content = content
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', text_content)
    return len(words)

if __name__ == "__main__":
    # File paths
    prompt_file = "Prompt.txt"
    tools_file = "Tools.json"
    
    # Count words in prompt file
    prompt_word_count = count_words_in_text(prompt_file)
    print(f"Total words in system prompt: {prompt_word_count}")
    
    # Count words in tools file
    tools_word_count = count_words_in_json_like_text(tools_file)
    print(f"Total words in tools definition: {tools_word_count}")
    
    # Total words
    total_words = prompt_word_count + tools_word_count
    print(f"Total words in system prompt and tools: {total_words}")
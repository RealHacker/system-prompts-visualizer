import re

def count_words_in_file(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def count_words_in_section(text):
    """Count words in a specific text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

if __name__ == "__main__":
    # Count words in both files
    prompt_words = count_words_in_file("Prompt Wave 11.txt")
    tools_words = count_words_in_file("Tools Wave 11.txt")
    
    total_words = prompt_words + tools_words
    
    print(f"Words in Prompt file: {prompt_words}")
    print(f"Words in Tools file: {tools_words}")
    print(f"Total words: {total_words}")
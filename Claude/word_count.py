import re

def count_words_in_text(file_path):
    """Count words in a text file."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def count_words_in_section(text):
    """Count words in a specific text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

if __name__ == "__main__":
    file_path = "Sonnet 4.5 Prompt.txt"
    total_words = count_words_in_text(file_path)
    print(f"Total words in system prompt: {total_words}")
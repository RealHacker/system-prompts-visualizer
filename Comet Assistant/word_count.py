import re

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def count_words_in_section(text):
    """Count words in a text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

if __name__ == "__main__":
    # Example usage
    prompt_file = "System Prompt.txt"
    
    prompt_word_count = count_words_in_text(prompt_file)
    
    print(f"Prompt word count: {prompt_word_count}")
import re

def count_words(text):
    """Count the number of words in a text string."""
    # Remove extra whitespace and split by whitespace
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_words_in_file(file_path):
    """Count words in a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return count_words(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python word_count.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    word_count = count_words_in_file(file_path)
    print(f"Total words in {file_path}: {word_count}")
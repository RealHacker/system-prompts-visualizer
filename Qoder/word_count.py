import re

def count_words(text):
    """Count the number of words in a text string."""
    # Remove extra whitespace and split by whitespace
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_words_in_file(file_path):
    """Count words in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return count_words(content)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return 0

if __name__ == "__main__":
    # Count words in each Qoder prompt file
    files = ["prompt.txt", "Quest Action.txt", "Quest Design.txt"]
    total_words = 0
    
    for file_name in files:
        file_path = f"{file_name}"
        word_count = count_words_in_file(file_path)
        print(f"{file_name}: {word_count} words")
        total_words += word_count
    
    print(f"\nTotal words in all Qoder prompt files: {total_words}")
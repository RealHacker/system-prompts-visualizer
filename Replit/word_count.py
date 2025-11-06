def count_words_in_file(file_path):
    """Count the total words in a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        words = content.split()
        return len(words)

if __name__ == "__main__":
    word_count = count_words_in_file("Prompt.txt")
    print(f"Total words in Prompt.txt: {word_count}")
def count_words_in_prompt(file_path):
    """Count the number of words in the prompt file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by whitespace and filter out empty strings
    words = [word for word in content.split() if word.strip()]
    return len(words)

if __name__ == "__main__":
    word_count = count_words_in_prompt("Prompt.txt")
    print(f"Total word count: {word_count}")
    
    # Save to a JSON file
    import json
    with open("word_count.json", "w") as f:
        json.dump({"word_count": word_count}, f)
import re

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

if __name__ == "__main__":
    # File paths
    default_prompt_file = "Default Prompt.txt"
    enterprise_prompt_file = "Enterprise Prompt.txt"
    
    # Count words in default prompt
    try:
        default_word_count = count_words_in_text(default_prompt_file)
        print(f"Words in {default_prompt_file}: {default_word_count}")
    except FileNotFoundError:
        print(f"File {default_prompt_file} not found")
        default_word_count = 0
    
    # Count words in enterprise prompt
    try:
        enterprise_word_count = count_words_in_text(enterprise_prompt_file)
        print(f"Words in {enterprise_prompt_file}: {enterprise_word_count}")
    except FileNotFoundError:
        print(f"File {enterprise_prompt_file} not found")
        enterprise_word_count = 0
    
    # Total word count
    total_word_count = default_word_count + enterprise_word_count
    print(f"Total words in all prompt files: {total_word_count}")
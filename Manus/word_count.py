import re
import json

def count_words(text):
    """Count the number of words in a text"""
    # Remove extra whitespace and split by whitespace
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_words_in_file(file_path):
    """Count words in a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return count_words(content)

def main():
    # Count words in each file
    prompt_words = count_words_in_file('Prompt.txt')
    modules_words = count_words_in_file('Modules.txt')
    agent_loop_words = count_words_in_file('Agent loop.txt')
    tools_words = count_words_in_file('tools.json')
    
    total_words = prompt_words + modules_words + agent_loop_words + tools_words
    
    print(f"Prompt.txt: {prompt_words} words")
    print(f"Modules.txt: {modules_words} words")
    print(f"Agent loop.txt: {agent_loop_words} words")
    print(f"tools.json: {tools_words} words")
    print(f"Total: {total_words} words")
    
    # Also load the analysis to verify
    try:
        with open('prompt_analysis.json', 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        print(f"Analysis total: {analysis['overview']['total_word_count']} words")
    except FileNotFoundError:
        print("prompt_analysis.json not found")

if __name__ == '__main__':
    main()
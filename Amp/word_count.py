import re
import yaml

def count_words_in_yaml(file_path):
    """Count words in a YAML file, focusing on the system prompt text."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the YAML to extract text content
    try:
        data = yaml.safe_load(content)
        
        # Extract all text content from the system prompt
        text_content = ""
        if 'system' in data:
            for item in data['system']:
                if isinstance(item, dict) and 'text' in item:
                    text_content += item['text'] + " "
        
        # Clean and count words
        # Remove extra whitespace and split into words
        words = re.findall(r'\b[a-zA-Z]+\b', text_content)
        return len(words)
    
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        # Fallback: count words in the raw text
        words = re.findall(r'\b[a-zA-Z]+\b', content)
        return len(words)

def count_words_in_section(text):
    """Count words in a specific text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

if __name__ == "__main__":
    file_path = "claude-4-sonnet.yaml"
    total_words = count_words_in_yaml(file_path)
    print(f"Total words in system prompt: {total_words}")
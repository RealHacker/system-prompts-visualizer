import re
import json

def count_words(text):
    """Count words in text"""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_sections(content):
    """Extract sections from the prompt based on headers"""
    sections = {}
    
    # Split content into lines
    lines = content.split('\n')
    
    current_section = "Introduction"
    current_text = ""
    
    for line in lines:
        # Check if line is a header (starts with # or ##)
        if line.strip().startswith('#'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = {
                    'content': current_text.strip(),
                    'word_count': count_words(current_text.strip())
                }
            
            # Start new section
            current_section = line.strip().strip('# ').strip()
            current_text = ""
        else:
            current_text += line + "\n"
    
    # Save the last section
    if current_text.strip():
        sections[current_section] = {
            'content': current_text.strip(),
            'word_count': count_words(current_text.strip())
        }
    
    return sections

def analyze_word_distribution(file_path):
    """Analyze word distribution in the prompt file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections with word counts
    sections = extract_sections(content)
    
    # Calculate total words
    total_words = sum(section['word_count'] for section in sections.values())
    
    # Create word count data for visualization
    word_count_data = []
    for section_name, section_data in sections.items():
        percentage = (section_data['word_count'] / total_words * 100) if total_words > 0 else 0
        word_count_data.append({
            'name': section_name,
            'words': section_data['word_count'],
            'percentage': round(percentage, 1)
        })
    
    # Sort by word count (descending)
    word_count_data.sort(key=lambda x: x['words'], reverse=True)
    
    return word_count_data, total_words

if __name__ == "__main__":
    file_path = "Prompt.txt"
    
    # Analyze word distribution
    word_count_data, total_words = analyze_word_distribution(file_path)
    
    # Save to JSON file
    with open('word_count.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_words': total_words,
            'sections': word_count_data
        }, f, indent=2)
    
    print(f"Total words: {total_words}")
    print("Word count data saved to word_count.json")
import re

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def extract_sections_and_content(file_path):
    """Extract sections from the system prompt text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on headers (lines starting with ##)
    sections = {}
    current_section = "Introduction"
    current_text = ""
    
    for line in content.split('\n'):
        if line.strip().startswith('##'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section
            current_section = line.strip().strip('# ').strip()
            current_text = ""
        else:
            current_text += line + "\n"
    
    # Save the last section
    if current_text.strip():
        sections[current_section] = current_text.strip()
    
    return sections

def extract_key_points(content):
    """Extract key points and rules from the content."""
    # Extract bullet points and numbered lists
    lines = content.split('\n')
    key_points = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('- ') or line.startswith('* ') or re.match(r'\d+\.', line):
            key_points.append(line)
    
    return key_points

def get_file_format(file_path):
    """Get the format of the file based on its extension."""
    if file_path.endswith('.txt'):
        return 'Plain Text'
    else:
        return 'Unknown'

def extract_role_and_identity(content):
    """Extract role and identity information."""
    role_info = {}
    
    # Look for role/identity information
    role_patterns = [
        r'You are.*?(?:an AI|AI assistant|agent|assistant)',
        r'Role.*?:.*?(?:an AI|AI assistant|agent|assistant)',
        r'Identity.*?:.*?(?:an AI|AI assistant|agent|assistant)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            role_info['role'] = match.group(0)
            break
    
    return role_info

if __name__ == "__main__":
    # File paths
    prompt_file = "System Prompt.txt"
    
    # Count words in prompt file
    prompt_word_count = count_words_in_text(prompt_file)
    print(f"Words in prompt file: {prompt_word_count}")
    
    # Get file formats
    prompt_format = get_file_format(prompt_file)
    print(f"Prompt file format: {prompt_format}")
    
    # Extract sections
    sections = extract_sections_and_content(prompt_file)
    print(f"\nNumber of sections in prompt: {len(sections)}")
    
    # Print section names
    print("Sections found:")
    for section_name in sections.keys():
        print(f"  - {section_name}")
    
    # Extract role information
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    role_info = extract_role_and_identity(content)
    print(f"\nRole information: {role_info}")
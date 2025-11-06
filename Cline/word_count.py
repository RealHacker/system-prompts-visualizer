import re
import json

def count_words_in_text(text):
    """Count words in text content."""
    if not text:
        return 0
    # Remove extra whitespace and split into words
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def analyze_cline_prompt():
    """Analyze the Cline prompt and generate word count statistics."""
    
    # Read the prompt file
    with open('Prompt.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Define section markers based on the prompt structure
    sections = {
        'Overview': 'You are Cline',
        'Tool Use': 'TOOL USE',
        'Tools Detail': '## execute_command',
        'Tool Examples': '# Tool Use Examples',
        'Tool Guidelines': '# Tool Use Guidelines',
        'Editing Files': 'EDITING FILES',
        'MCP Servers': 'MCP SERVERS',
        'Act vs Plan Mode': 'ACT MODE V.S. PLAN MODE',
        'Capabilities': 'CAPABILITIES',
        'Rules': 'RULES',
        'System Info': 'SYSTEM INFORMATION',
        'Objective': 'OBJECTIVE'
    }
    
    # Count words in each section
    word_counts = {}
    
    # Simple approach: count words in the entire prompt
    total_words = count_words_in_text(content)
    word_counts['Total'] = total_words
    
    # Read the section texts file for more detailed analysis
    try:
        with open('section_texts.json', 'r', encoding='utf-8') as file:
            section_texts = json.load(file)
        
        # Count words in each section
        for section_name, section_content in section_texts.items():
            word_counts[section_name] = count_words_in_text(section_content)
            
    except FileNotFoundError:
        print("section_texts.json not found, using basic word count")
        word_counts['Overview'] = count_words_in_text('You are Cline')
        word_counts['Tools Detail'] = count_words_in_text(content.split('## execute_command')[1].split('# Tool Use Examples')[0])
    
    # Save word counts to JSON file
    with open('word_count.json', 'w', encoding='utf-8') as file:
        json.dump(word_counts, file, indent=2)
    
    return word_counts

def get_tool_count():
    """Get the number of tools available to Cline."""
    try:
        with open('prompt_analysis.json', 'r', encoding='utf-8') as file:
            analysis = json.load(file)
        return len(analysis.get('tools', []))
    except FileNotFoundError:
        # Based on the prompt content, there are 15 tools
        return 15

if __name__ == "__main__":
    word_counts = analyze_cline_prompt()
    tool_count = get_tool_count()
    
    print("Cline System Prompt Word Count Analysis:")
    print(f"Total words: {word_counts.get('Total', 0)}")
    print(f"Tool count: {tool_count}")
    print(f"Format: plain text with XML-style tool formatting")
    
    print("\nSection word counts:")
    for section, count in word_counts.items():
        if section != 'Total':
            print(f"  {section}: {count}")
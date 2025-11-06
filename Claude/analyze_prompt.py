import re

def extract_sections_and_count_words(text_content):
    """Extract sections from the text system prompt and count words in each."""
    
    # Extract sections based on headers (lines starting with # or in XML tags)
    sections = {}
    current_section = "Overview"
    current_text = ""
    
    for line in text_content.split('\n'):
        # Look for section headers (XML tags or markdown-style headers)
        if line.strip().startswith('<') and '>' in line.strip() and not line.strip().startswith('</'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section - extract tag name
            tag_match = re.match(r'<([^>]+)>', line.strip())
            if tag_match:
                current_section = tag_match.group(1).replace('_', ' ').title()
                current_text = ""
        elif line.strip().startswith('#'):
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
    
    # Count words in each section
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_text in sections.items():
        words = re.findall(r'\b[a-zA-Z]+\b', section_text)
        word_count = len(words)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    return sections, section_word_counts, total_words

def count_words_in_section(text):
    """Count words in a specific text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_tool_info(text_content):
    """Extract information about tools from the prompt."""
    # Look for tool-related sections
    tools_info = []
    
    # Check if there are tools mentioned in artifacts section
    if 'artifacts_info' in text_content or 'artifact_instructions' in text_content:
        tool_info = {
            'name': 'Artifacts',
            'description': 'Create and reference artifacts during conversations for substantial code, analysis, and writing'
        }
        tools_info.append(tool_info)
    
    if 'search_instructions' in text_content or 'web_search' in text_content:
        tool_info = {
            'name': 'Web Search',
            'description': 'Search the web for information past knowledge cutoff or current events'
        }
        tools_info.append(tool_info)
    
    return tools_info

def count_tools(text_content):
    """Count the number of tools mentioned in the prompt."""
    tools = extract_tool_info(text_content)
    return len(tools)

if __name__ == "__main__":
    # Read the Sonnet 4.5 prompt
    file_path = "Sonnet 4.5 Prompt.txt"
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections and count words
    sections, section_word_counts, total_words = extract_sections_and_count_words(content)
    
    # Count tools
    tool_count = count_tools(content)
    
    # Extract tool information
    tools_info = extract_tool_info(content)
    
    print(f"=== SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Number of tools: {tool_count}")
    print(f"Format: Plain Text")
    print()
    
    print("=== SECTION WORD COUNTS ===")
    for section, count in section_word_counts.items():
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        print(f"{section}: {count} words ({percentage:.1f}%)")
    
    print()
    print("=== TOOL INFORMATION ===")
    for tool in tools_info:
        print(f"Tool: {tool['name']}")
        print(f"Description: {tool['description']}")
        print()
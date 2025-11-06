import re
import os

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
    
    # Extract sections based on headers (lines starting with # or tags like <tag>)
    sections = {}
    current_section = "Introduction"
    current_text = ""
    
    for line in content.split('\n'):
        # Check for section headers (markdown-style headers)
        if line.strip().startswith('#'):
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

def count_words_in_section(text):
    """Count words in a specific text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_section_word_counts(sections):
    """Count words in each section."""
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_text in sections.items():
        word_count = count_words_in_section(section_text)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    return section_word_counts, total_words

def extract_role_and_identity(content):
    """Extract role and identity information."""
    # Look for role/identity information
    role_patterns = [
        r'You are.*?(?:an AI|AI assistant|agent|assistant|engineer)',
        r'Role.*?:.*?(?:an AI|AI assistant|agent|assistant|engineer)',
        r'Identity.*?:.*?(?:an AI|AI assistant|agent|assistant|engineer)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return "Software engineer AI agent"

def extract_context_window(content):
    """Extract context window information if present."""
    # Look for context window information
    context_patterns = [
        r'context\s+window.*?(\d+)',
        r'context.*?limit.*?(\d+)',
        r'(\d+)\s+token.*?context',
        r'context.*?(\d+)\s+token'
    ]
    
    for pattern in context_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return f"{match.group(1)} tokens"
    
    return "Not specified"

def get_file_format(file_path):
    """Get the format of the file based on its extension."""
    if file_path.endswith('.txt'):
        return 'Plain Text'
    else:
        return 'Unknown'

def extract_agentic_workflow(sections):
    """Extract information about the agentic workflow."""
    workflow_info = ""
    
    # Look for workflow-related sections
    workflow_keywords = ['workflow', 'approach', 'process', 'task', 'work']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in workflow_keywords):
            workflow_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return workflow_info.strip() if workflow_info else "Not explicitly defined"

def extract_rules(sections):
    """Extract rules and guidelines."""
    rules_info = ""
    
    # Look for rules-related sections
    rules_keywords = ['rule', 'guideline', 'principle', 'limitation', 'constraint']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in rules_keywords):
            rules_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return rules_info.strip() if rules_info else "Not explicitly defined in separate section"

def extract_context_management(sections):
    """Extract context management information."""
    context_info = ""
    
    # Look for context-related sections
    context_keywords = ['context', 'information', 'data', 'memory']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in context_keywords):
            context_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return context_info.strip() if context_info else "Not explicitly defined"

def extract_coding_standards(sections):
    """Extract coding standards and best practices."""
    coding_info = ""
    
    # Look for coding-related sections
    coding_keywords = ['coding', 'code', 'programming', 'standard', 'practice', 'style']
    for section_name, section_content in sections.items():
        if any(keyword in section_name.lower() for keyword in coding_keywords):
            coding_info += f"Section: {section_name}\n{section_content}\n\n"
    
    return coding_info.strip() if coding_info else "Not explicitly defined"

def extract_tools_info(content):
    """Extract information about tools mentioned in the prompt."""
    tools_info = []
    
    # Look for tool-related sections or mentions
    tool_section_patterns = [
        r'<(\w+)',
        r'command.*?:',
        r'tool.*?:'
    ]
    
    tool_matches = []
    for pattern in tool_section_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        tool_matches.extend(matches)
    
    # Remove duplicates and filter meaningful tool names
    unique_tools = list(set([tool for tool in tool_matches if len(tool) > 2]))
    
    for tool in unique_tools[:10]:  # Limit to first 10 tools
        tools_info.append({
            'name': tool,
            'description': 'Tool mentioned in system prompt'
        })
    
    return tools_info

if __name__ == "__main__":
    # File paths
    prompt_file = "Prompt.txt"
    
    # Count words in prompt file
    prompt_word_count = count_words_in_text(prompt_file)
    print(f"Words in prompt file: {prompt_word_count}")
    
    # Get file format
    prompt_format = get_file_format(prompt_file)
    print(f"Prompt file format: {prompt_format}")
    
    # Extract sections
    sections = extract_sections_and_content(prompt_file)
    print(f"\nNumber of sections in prompt: {len(sections)}")
    
    # Count words in each section
    section_word_counts, total_words = extract_section_word_counts(sections)
    print(f"Total words counted in sections: {total_words}")
    
    # Extract role information
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    role_info = extract_role_and_identity(content)
    print(f"Role information: {role_info}")
    
    # Extract context window
    context_window = extract_context_window(content)
    print(f"Context window: {context_window}")
    
    # Extract agentic workflow
    workflow_info = extract_agentic_workflow(sections)
    print(f"Workflow info extracted")
    
    # Extract rules
    rules_info = extract_rules(sections)
    print(f"Rules info extracted")
    
    # Extract context management
    context_info = extract_context_management(sections)
    print(f"Context management info extracted")
    
    # Extract coding standards
    coding_info = extract_coding_standards(sections)
    print(f"Coding standards info extracted")
    
    # Extract tools
    tools_info = extract_tools_info(content)
    print(f"Extracted information for {len(tools_info)} tools")
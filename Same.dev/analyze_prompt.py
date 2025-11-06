import json
import re
import os

def count_words(text):
    """Count words in text"""
    return len(text.split())

def extract_sections(prompt_text):
    """Extract major sections from the prompt"""
    sections = {}
    
    # Define section patterns
    section_patterns = {
        'overview': r'(Knowledge cutoff.*?)(?=<.*?>|\Z)',
        'service_policies': r'<service_policies>(.*?)</service_policies>',
        'communication': r'<communication>(.*?)</communication>',
        'tool_calling': r'<tool_calling>(.*?)</tool_calling>',
        'maximize_parallel_tool_calls': r'<maximize_parallel_tool_calls>(.*?)</maximize_parallel_tool_calls>',
        'memos': r'<memos>(.*?)</memos>',
        'making_code_changes': r'<making_code_changes>(.*?)</making_code_changes>',
        'web_development': r'<web_development>(.*?)</web_development>',
        'web_design': r'<web_design>(.*?)</web_design>',
        'debugging': r'<debugging>(.*?)</debugging>',
        'website_cloning': r'<website_cloning>(.*?)</website_cloning>',
        'task_agent': r'<task_agent>(.*?)</task_agent>'
    }
    
    # Extract sections
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, prompt_text, re.DOTALL)
        if match:
            sections[section_name] = match.group(1).strip()
    
    return sections

def analyze_tools(tools_data):
    """Analyze tools from JSON data"""
    tools_info = {
        'total_tools': len(tools_data),
        'tools_list': []
    }
    
    for tool in tools_data:
        tool_info = {
            'name': tool.get('name', ''),
            'description': tool.get('description', ''),
            'parameters': tool.get('parameters', {})
        }
        tools_info['tools_list'].append(tool_info)
    
    return tools_info

def analyze_prompt_structure(prompt_text):
    """Analyze the structure of the prompt"""
    structure = {
        'total_words': count_words(prompt_text),
        'format': 'plain text with XML tags',
        'sections_count': len(re.findall(r'<.*?>', prompt_text)) // 2
    }
    return structure

def generate_analysis():
    """Main function to generate analysis"""
    # Read prompt file
    with open('Prompt.txt', 'r', encoding='utf-8') as f:
        prompt_text = f.read()
    
    # Read tools file
    with open('Tools.json', 'r', encoding='utf-8') as f:
        tools_data = json.load(f)
    
    # Extract sections
    sections = extract_sections(prompt_text)
    
    # Analyze tools
    tools_info = analyze_tools(tools_data)
    
    # Analyze structure
    structure_info = analyze_prompt_structure(prompt_text)
    
    # Create analysis
    analysis = {
        'overview': {
            'role': 'AI coding assistant and agent manager powered by gpt-4.1 operating in Same cloud-based IDE',
            'total_word_count': structure_info['total_words'],
            'format': structure_info['format'],
            'total_tools': tools_info['total_tools']
        },
        'sections': sections,
        'tools': tools_info,
        'structure': structure_info
    }
    
    # Save analysis
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    return analysis

if __name__ == "__main__":
    analysis = generate_analysis()
    print("Analysis complete. Results saved to prompt_analysis.json")
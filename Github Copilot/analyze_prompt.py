#!/usr/bin/env python3
"""
Analyze GitHub Copilot system prompts and generate structured data for visualization.
"""

import os
import re
import json
from typing import Dict, List, Any

def read_file(file_path: str) -> str:
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

def extract_sections(content: str) -> Dict[str, str]:
    """Extract sections from the prompt content."""
    sections = {}
    
    # Look for XML-like tags
    tag_pattern = r'<(\w+)>(.*?)</\1>'
    matches = re.finditer(tag_pattern, content, re.DOTALL)
    
    for match in matches:
        tag_name = match.group(1)
        tag_content = match.group(2).strip()
        sections[tag_name] = tag_content
    
    # If no XML tags found, treat the whole content as one section
    if not sections:
        sections['main'] = content
    
    return sections

def analyze_tools(content: str) -> List[Dict[str, Any]]:
    """Extract tool information from the prompt."""
    tools = []
    
    # Look for tool/function definitions in JSON format
    functions_match = re.search(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
    if functions_match:
        try:
            functions_json = functions_match.group(0)
            # Fix JSON formatting issues
            functions_json = functions_json.replace('\n', '').replace('\t', '')
            functions_json = re.sub(r',\s*]', ']', functions_json)
            functions_json = re.sub(r',\s*}', '}', functions_json)
            
            tool_list = json.loads(functions_json)
            for tool in tool_list:
                if isinstance(tool, dict) and 'name' in tool:
                    tools.append({
                        'name': tool.get('name', 'Unknown'),
                        'description': tool.get('description', 'No description provided'),
                        'parameters': tool.get('parameters', {})
                    })
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract tool names manually
            tool_names = re.findall(r'"name":\s*"([^"]+)"', content)
            for name in tool_names:
                tools.append({
                    'name': name,
                    'description': 'Tool description not parsed',
                    'parameters': {}
                })
    
    return tools

def analyze_github_copilot_prompts() -> Dict[str, Any]:
    """Analyze GitHub Copilot prompt files and generate structured data."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Read prompt files
    prompt_file = os.path.join(script_dir, 'Prompt.txt')
    gpt5_file = os.path.join(script_dir, 'gpt-5.txt')
    
    prompt_content = read_file(prompt_file)
    gpt5_content = read_file(gpt5_file)
    
    # Extract sections
    prompt_sections = extract_sections(prompt_content)
    gpt5_sections = extract_sections(gpt5_content)
    
    # Combine sections
    all_sections = {**prompt_sections, **gpt5_sections}
    
    # Analyze tools
    prompt_tools = analyze_tools(prompt_content)
    gpt5_tools = analyze_tools(gpt5_content)
    all_tools = prompt_tools + gpt5_tools
    
    # Remove duplicates
    unique_tools = []
    seen_names = set()
    for tool in all_tools:
        if tool['name'] not in seen_names:
            unique_tools.append(tool)
            seen_names.add(tool['name'])
    
    # Generate word counts
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_content in all_sections.items():
        word_count = count_words(section_content)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    # Create analysis result
    analysis = {
        'overview': {
            'role': 'AI programming assistant for VS Code',
            'total_word_count': total_words,
            'number_of_tools': len(unique_tools),
            'format': 'XML-like structured text with JSON function definitions',
            'global_info': 'GitHub Copilot system prompts with detailed tool definitions and instructions'
        },
        'workflow': {
            'description': 'GitHub Copilot follows a structured approach to assist with programming tasks',
            'steps': [
                'Analyze user requests and context',
                'Use available tools to gather information',
                'Provide concise, helpful responses',
                'Follow Microsoft content policies',
                'Maintain expert-level knowledge across programming languages'
            ]
        },
        'tools': unique_tools,
        'context_management': {
            'description': 'Context management in GitHub Copilot',
            'details': [
                'Uses user requests and attached files as context',
                'Provides tools for file operations, searches, and code analysis',
                'Manages workspace information and environment context'
            ]
        },
        'rules': {
            'description': 'Rules and guidelines for GitHub Copilot behavior',
            'guidelines': [
                'Respond with "GitHub Copilot" when asked for name',
                'Follow Microsoft content policies',
                'Avoid harmful or inappropriate content',
                'Keep answers short and impersonal',
                'Use tools appropriately and efficiently'
            ]
        },
        'coding_standards': {
            'description': 'Coding standards and practices',
            'standards': [
                'Expert-level knowledge across programming languages',
                'Follow best practices for code editing and file operations',
                'Use appropriate tools for specific tasks',
                'Maintain code quality and correctness'
            ]
        },
        'other_info': {
            'description': 'Additional information about GitHub Copilot',
            'details': [
                'Works within VS Code editor environment',
                'Has access to various tools for file operations and code analysis',
                'Designed to be a helpful programming assistant'
            ]
        },
        'section_word_counts': section_word_counts
    }
    
    return analysis

def save_analysis(analysis: Dict[str, Any], output_file: str):
    """Save the analysis to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    # Perform analysis
    analysis_result = analyze_github_copilot_prompts()
    
    # Save to file
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prompt_analysis.json')
    save_analysis(analysis_result, output_file)
    
    print(f"Analysis complete. Results saved to {output_file}")
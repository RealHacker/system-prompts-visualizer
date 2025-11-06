import json
import re
from collections import defaultdict

def count_words(text):
    """Count words in text"""
    # Remove code blocks and count words
    # Remove code blocks first
    text_without_code = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text_without_code = re.sub(r'`[^`]*`', '', text_without_code)
    # Count words
    words = re.findall(r'\b\w+\b', text_without_code)
    return len(words)

def extract_sections(prompt_text):
    """Extract major sections from the prompt"""
    sections = {}
    
    # Overview section - the beginning of the document
    overview_match = re.search(r'You are v0, Vercel\'s highly skilled AI-powered assistant.*?(?=\n#{2,})', prompt_text, re.DOTALL)
    if overview_match:
        sections['overview'] = overview_match.group(0).strip()
    
    # Find all major sections (## or ### headers)
    section_pattern = r'(#{2,})\s+(.*?)(?=\n#{2,}|\Z)'
    section_matches = re.finditer(section_pattern, prompt_text, re.DOTALL)
    
    for match in section_matches:
        header_level = len(match.group(1))
        header_title = match.group(2).strip()
        # Get content until next section or end of file
        content_start = match.end()
        next_section = re.search(r'\n#{2,}', prompt_text[content_start:], re.DOTALL)
        if next_section:
            content = prompt_text[content_start:content_start + next_section.start()].strip()
        else:
            content = prompt_text[content_start:].strip()
        
        # Normalize header title for consistent keys
        normalized_title = header_title.lower().replace(' ', '_').replace('-', '_')
        sections[normalized_title] = {
            'title': header_title,
            'content': content,
            'level': header_level
        }
    
    return sections

def analyze_tools(tools_data):
    """Analyze tools from JSON data"""
    tools_info = []
    if 'tools' in tools_data:
        for tool in tools_data['tools']:
            tool_info = {
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'parameters': tool.get('parameters', {})
            }
            tools_info.append(tool_info)
    return tools_info

def extract_agentic_workflow(sections):
    """Extract agentic workflow information"""
    workflow_info = []
    
    # Look for workflow-related sections
    workflow_keywords = ['workflow', 'process', 'steps', 'task', 'execution']
    for section_key, section_data in sections.items():
        if isinstance(section_data, dict) and 'title' in section_data:
            title = section_data['title'].lower()
            if any(keyword in title for keyword in workflow_keywords):
                workflow_info.append({
                    'section': section_data['title'],
                    'content': section_data['content']
                })
    
    return workflow_info

def extract_rules(sections):
    """Extract rules and guidelines"""
    rules = []
    
    # Look for rules, guidelines, or constraint sections
    rule_keywords = ['rule', 'guideline', 'constraint', 'must', 'should', 'never', 'always']
    for section_key, section_data in sections.items():
        if isinstance(section_data, dict) and 'content' in section_data:
            content = section_data['content'].lower()
            # Check if section contains many rule-like statements
            rule_count = sum(1 for keyword in rule_keywords if keyword in content)
            if rule_count > 3 or any(keyword in section_data.get('title', '').lower() for keyword in ['rule', 'guideline']):
                rules.append({
                    'section': section_data.get('title', section_key),
                    'content': section_data['content']
                })
    
    return rules

def extract_context_management(sections):
    """Extract context management information"""
    context_info = []
    
    # Look for context-related sections
    context_keywords = ['context', 'memory', 'history', 'conversation', 'state']
    for section_key, section_data in sections.items():
        if isinstance(section_data, dict) and 'title' in section_data:
            title = section_data['title'].lower()
            if any(keyword in title for keyword in context_keywords):
                context_info.append({
                    'section': section_data['title'],
                    'content': section_data['content']
                })
    
    return context_info

def extract_coding_standards(sections):
    """Extract coding standards and design guidelines"""
    coding_info = []
    
    # Look for coding/design related sections
    coding_keywords = ['coding', 'design', 'style', 'component', 'ui', 'layout', 'tailwind', 'react']
    for section_key, section_data in sections.items():
        if isinstance(section_data, dict) and 'title' in section_data:
            title = section_data['title'].lower()
            if any(keyword in title for keyword in coding_keywords):
                coding_info.append({
                    'section': section_data['title'],
                    'content': section_data['content']
                })
    
    return coding_info

def main():
    # Read prompt file
    with open('Prompt.txt', 'r', encoding='utf-8') as f:
        prompt_text = f.read()
    
    # Read tools file
    with open('Tools.json', 'r', encoding='utf-8') as f:
        tools_data = json.load(f)
    
    # Analyze prompt
    total_words = count_words(prompt_text)
    sections = extract_sections(prompt_text)
    
    # Analyze tools
    tools_info = analyze_tools(tools_data)
    
    # Extract specific information
    workflow_info = extract_agentic_workflow(sections)
    rules_info = extract_rules(sections)
    context_info = extract_context_management(sections)
    coding_info = extract_coding_standards(sections)
    
    # Create analysis result
    analysis = {
        'overview': {
            'role': 'Vercel\'s highly skilled AI-powered assistant that always follows best practices',
            'total_words': total_words,
            'format': 'Plain text with markdown formatting',
            'tools_count': len(tools_info)
        },
        'workflow': workflow_info,
        'tools': tools_info,
        'context_management': context_info,
        'rules': rules_info,
        'coding_standards': coding_info,
        'other_info': []
    }
    
    # Save analysis
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Total words: {total_words}")
    print(f"Sections found: {len(sections)}")
    print(f"Tools found: {len(tools_info)}")

if __name__ == '__main__':
    main()
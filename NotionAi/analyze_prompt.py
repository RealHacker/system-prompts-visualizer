import json
import re

def count_words(text):
    """Count the number of words in a text"""
    return len(text.split())

def extract_sections(prompt_text):
    """Extract major sections from the prompt"""
    sections = {}
    
    # Overview section
    overview_match = re.search(r'You are Notion AI, an AI agent inside of Notion\.(.*?)<tool calling spec>', prompt_text, re.DOTALL)
    if overview_match:
        sections['overview'] = overview_match.group(1).strip()
    
    # Tool calling spec
    tool_spec_match = re.search(r'<tool calling spec>(.*?)</tool calling spec>', prompt_text, re.DOTALL)
    if tool_spec_match:
        sections['tool_calling_spec'] = tool_spec_match.group(1).strip()
    
    # Main concepts
    concepts_match = re.search(r'</tool calling spec>\s*(.*?)### Pages', prompt_text, re.DOTALL)
    if concepts_match:
        sections['main_concepts'] = concepts_match.group(1).strip()
    
    # Pages section
    pages_match = re.search(r'### Pages(.*?)### Databases', prompt_text, re.DOTALL)
    if pages_match:
        sections['pages'] = pages_match.group(1).strip()
    
    # Databases section
    databases_match = re.search(r'### Databases(.*?)### Format and style for direct chat responses', prompt_text, re.DOTALL)
    if databases_match:
        sections['databases'] = databases_match.group(1).strip()
    
    # Format and style
    format_match = re.search(r'### Format and style for direct chat responses(.*?)### Format and style for drafting and editing content', prompt_text, re.DOTALL)
    if format_match:
        sections['format_chat'] = format_match.group(1).strip()
    
    # Drafting and editing format
    drafting_match = re.search(r'### Format and style for drafting and editing content(.*?)### Search', prompt_text, re.DOTALL)
    if drafting_match:
        sections['format_drafting'] = drafting_match.group(1).strip()
    
    # Search section
    search_match = re.search(r'### Search(.*?)### Refusals', prompt_text, re.DOTALL)
    if search_match:
        sections['search'] = search_match.group(1).strip()
    
    # Refusals section
    refusals_match = re.search(r'### Refusals(.*?)### Avoid offering to do things', prompt_text, re.DOTALL)
    if refusals_match:
        sections['refusals'] = refusals_match.group(1).strip()
    
    # Avoid offering section
    avoid_offering_match = re.search(r'### Avoid offering to do things(.*?)### IMPORTANT: Avoid overperforming', prompt_text, re.DOTALL)
    if avoid_offering_match:
        sections['avoid_offering'] = avoid_offering_match.group(1).strip()
    
    # Avoid overperforming
    avoid_overperforming_match = re.search(r'### IMPORTANT: Avoid overperforming(.*?)### Be gender neutral', prompt_text, re.DOTALL)
    if avoid_overperforming_match:
        sections['avoid_overperforming'] = avoid_overperforming_match.group(1).strip()
    
    # Gender neutrality
    gender_neutral_match = re.search(r'### Be gender neutral.*?--- END OF EXAMPLES ---(.*?)### Notion-flavored Markdown', prompt_text, re.DOTALL)
    if gender_neutral_match:
        sections['gender_neutral'] = gender_neutral_match.group(1).strip()
    
    # Notion-flavored Markdown
    markdown_match = re.search(r'### Notion-flavored Markdown(.*?)<context>', prompt_text, re.DOTALL)
    if markdown_match:
        sections['notion_markdown'] = markdown_match.group(1).strip()
    
    return sections

def analyze_tools(tools_data):
    """Analyze the tools JSON data"""
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

def generate_analysis():
    """Generate the complete analysis"""
    # Read prompt file
    with open('Prompt.txt', 'r', encoding='utf-8') as f:
        prompt_text = f.read()
    
    # Read tools file
    with open('tools.json', 'r', encoding='utf-8') as f:
        tools_data = json.load(f)
    
    # Analyze prompt
    sections = extract_sections(prompt_text)
    
    # Analyze tools
    tools_info = analyze_tools(tools_data)
    
    # Count words in prompt
    total_words = count_words(prompt_text)
    
    # Create analysis dictionary
    analysis = {
        'stats': {
            'total_words': total_words,
            'total_tools': tools_info['total_tools'],
            'format': 'Plain text + JSON'
        },
        'overview': {
            'role': 'Notion AI is an AI agent inside of Notion that interacts via a chat interface.',
            'stats': {
                'total_words': total_words,
                'total_tools': tools_info['total_tools'],
                'format': 'Plain text + JSON'
            }
        },
        'workflow': {
            'description': 'Notion AI works by receiving user messages and using tools in a loop until it ends the loop by responding without tool calls.',
            'steps': [
                'Receive user message',
                'Use tools in a loop as needed',
                'End loop by responding without tool calls'
            ]
        },
        'tools': tools_info,
        'sections': sections
    }
    
    # Save analysis to JSON file
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    return analysis

if __name__ == '__main__':
    analysis = generate_analysis()
    print("Analysis complete. Results saved to prompt_analysis.json")
import re
import json
from xml.etree import ElementTree as ET

def analyze_perplexity_prompt(file_path):
    """Analyze the Perplexity system prompt and extract structured information."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the XML-like structure
    # Extract sections by tags
    sections = {}
    
    # Overview section
    goal_match = re.search(r'<goal>(.*?)</goal>', content, re.DOTALL)
    if goal_match:
        sections['overview'] = {
            'role': goal_match.group(1).strip(),
            'format': 'XML-like structured format'
        }
    
    # Format rules section
    format_match = re.search(r'<format_rules>(.*?)</format_rules>', content, re.DOTALL)
    if format_match:
        sections['format_rules'] = format_match.group(1).strip()
    
    # Restrictions section
    restrictions_match = re.search(r'<restrictions>(.*?)</restrictions>', content, re.DOTALL)
    if restrictions_match:
        sections['restrictions'] = restrictions_match.group(1).strip()
    
    # Query type section
    query_type_match = re.search(r'<query_type>(.*?)</query_type>', content, re.DOTALL)
    if query_type_match:
        sections['query_type'] = query_type_match.group(1).strip()
    
    # Planning rules section
    planning_rules_match = re.search(r'<planning_rules>(.*?)</planning_rules>', content, re.DOTALL)
    if planning_rules_match:
        sections['planning_rules'] = planning_rules_match.group(1).strip()
    
    # Output section
    output_match = re.search(r'<output>(.*?)</output>', content, re.DOTALL)
    if output_match:
        sections['output'] = output_match.group(1).strip()
    
    # Count words
    word_count = len(content.split())
    
    # Compile overview information
    if 'overview' in sections:
        sections['overview']['word_count'] = word_count
        sections['overview']['tool_count'] = 0  # No explicit tools in this prompt
    
    return sections

def save_analysis(sections, output_path):
    """Save the analysis to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    prompt_file = "Prompt.txt"
    analysis = analyze_perplexity_prompt(prompt_file)
    save_analysis(analysis, "prompt_analysis.json")
    print("Analysis complete. Results saved to prompt_analysis.json")
import json
import re
from collections import defaultdict

def count_words(text):
    """Count words in text"""
    # Remove extra whitespace and split
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def extract_sections_from_prompt(prompt_text):
    """Extract sections from the prompt text"""
    sections = {}
    
    # Define patterns for different sections
    patterns = {
        'role': r'<role>(.*?)</role>',
        'communication': r'<communication>(.*?)</communication>',
        'limitations': r'<limitations>(.*?)</limitations>',
        'decision_tree': r'<decision_tree>(.*?)</decision_tree>',
        'general_guidelines': r'<general_guidelines>(.*?)</general_guidelines>',
        'coding_guidelines': r'<coding_guidelines>(.*?)</coding_guidelines>',
        'important': r'<important>(.*?)</important>',
        'internal_monologue': r'<internal_monologue>(.*?)</internal_monologue>',
        'coding_best_practices': r'<coding_best_practices>(.*?)</coding_best_practices>',
        'information_handling': r'<information_handling>(.*?)</information_handling>',
        'hand_over_to_approach_agent_tool_call': r'<hand_over_to_approach_agent_tool_call>(.*?)</hand_over_to_approach_agent_tool_call>',
        'do_not_hand_over_to_approach_agent': r'<do_not_hand_over_to_approach_agent>(.*?)</do_not_hand_over_to_approach_agent>'
    }
    
    # Extract sections using patterns
    for section_name, pattern in patterns.items():
        match = re.search(pattern, prompt_text, re.DOTALL)
        if match:
            sections[section_name] = match.group(1).strip()
    
    return sections

def analyze_tools(tools_data):
    """Analyze tools from JSON data"""
    tools_info = []
    
    for tool_name, tool_data in tools_data.items():
        tool_info = {
            'name': tool_name,
            'description': tool_data.get('description', ''),
            'parameters': tool_data.get('parameters', {})
        }
        tools_info.append(tool_info)
    
    return tools_info

def analyze_phase_mode():
    """Analyze phase mode prompt and tools"""
    # Read phase mode prompt
    with open('phase_mode_prompts.txt', 'r', encoding='utf-8') as f:
        phase_prompt = f.read()
    
    # Read phase mode tools (fixed version)
    with open('phase_mode_tools_fixed.json', 'r', encoding='utf-8') as f:
        phase_tools = json.load(f)
    
    # Extract sections
    sections = extract_sections_from_prompt(phase_prompt)
    
    # Analyze tools
    tools_info = analyze_tools(phase_tools)
    
    # Count words
    total_words = count_words(phase_prompt)
    
    return {
        'mode': 'Phase Mode',
        'sections': sections,
        'tools': tools_info,
        'total_words': total_words,
        'format': 'XML/JSON'
    }

def analyze_plan_mode():
    """Analyze plan mode prompt and tools"""
    # Read plan mode prompt
    with open('plan_mode_prompts', 'r', encoding='utf-8') as f:
        plan_prompt = f.read()
    
    # Read plan mode tools (fixed version)
    with open('plan_mode_tools_fixed.json', 'r', encoding='utf-8') as f:
        plan_tools = json.load(f)
    
    # Extract sections
    sections = extract_sections_from_prompt(plan_prompt)
    
    # Analyze tools
    tools_info = analyze_tools(plan_tools)
    
    # Count words
    total_words = count_words(plan_prompt)
    
    return {
        'mode': 'Plan Mode',
        'sections': sections,
        'tools': tools_info,
        'total_words': total_words,
        'format': 'XML/JSON'
    }

def generate_analysis():
    """Generate complete analysis for both modes"""
    phase_analysis = analyze_phase_mode()
    plan_analysis = analyze_plan_mode()
    
    # Combine analyses
    combined_analysis = {
        'phase_mode': phase_analysis,
        'plan_mode': plan_analysis,
        'overall_stats': {
            'total_words': phase_analysis['total_words'] + plan_analysis['total_words'],
            'total_tools': len(phase_analysis['tools']) + len(plan_analysis['tools'])
        }
    }
    
    # Save to file
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(combined_analysis, f, indent=2, ensure_ascii=False)
    
    return combined_analysis

if __name__ == "__main__":
    analysis = generate_analysis()
    print("Analysis complete. Results saved to prompt_analysis.json")
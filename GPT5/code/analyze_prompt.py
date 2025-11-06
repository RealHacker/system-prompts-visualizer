#!/usr/bin/env python3
"""
GPT5 System Prompt Analyzer
Extracts and organizes system prompt into 7 required sections.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def load_prompt(filepath: str) -> str:
    """Load the system prompt text from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    """Count words accurately in the text."""
    # Remove code blocks and technical markup for accurate counting
    clean_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    clean_text = re.sub(r'`[^`]*`', '', clean_text)
    clean_text = re.sub(r'<[^>]*>', '', clean_text)
    clean_text = re.sub(r'{[^}]*}', '', clean_text)
    words = clean_text.split()
    return len([w for w in words if w.strip()])

def identify_tools(text: str) -> List[str]:
    """Identify and extract tool definitions from the prompt."""
    tools = []
    # Look for tool definitions in ## or ### sections
    tool_pattern = r'^##?\s*([a-zA-Z_][a-zA-Z0-9_]*)'
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if re.match(tool_pattern, line.strip()):
            tool_name = re.match(tool_pattern, line.strip()).group(1)
            # Skip if it's a subsection title like "When to use"
            if not any(keyword in line.lower() for keyword in ['when', 'when to', 'when not']):
                tools.append(tool_name)
    
    return tools

def detect_format(text: str) -> str:
    """Detect the format of the system prompt."""
    # Check for various formatting indicators
    has_json = bool(re.search(r'{\s*"[^"]+"\s*:', text))
    has_xml = bool(re.search(r'<[^>]+>', text))
    has_yaml = bool(re.search(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*.+', text, re.MULTILINE))
    has_code_blocks = bool(re.search(r'```', text))
    
    formats = []
    if has_json: formats.append("JSON")
    if has_xml: formats.append("XML-like")
    if has_yaml: formats.append("YAML-like")
    if has_code_blocks: formats.append("Code blocks")
    
    if not formats:
        return "Plain text"
    
    return " + ".join(formats)

def extract_overview(text: str) -> Dict[str, any]:
    """Extract overview information from the prompt."""
    lines = text.split('\n')
    overview = {}
    
    # Extract agent role/identity
    role_lines = []
    for i, line in enumerate(lines):
        if 'You are ChatGPT' in line or 'based on the GPT-5 model' in line:
            role_lines.append(line.strip())
            # Include next few lines for context
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip() and not lines[j].startswith('#'):
                    role_lines.append(lines[j].strip())
                else:
                    break
            break
    
    overview['role'] = ' '.join(role_lines) if role_lines else "ChatGPT - Large Language Model"
    overview['word_count'] = count_words(text)
    overview['tool_count'] = len(identify_tools(text))
    overview['format'] = detect_format(text)
    overview['knowledge_cutoff'] = None
    overview['current_date'] = None
    
    # Extract metadata
    for line in lines[:10]:
        if 'Knowledge cutoff:' in line:
            overview['knowledge_cutoff'] = line.split(':', 1)[1].strip()
        if 'Current date:' in line:
            overview['current_date'] = line.split(':', 1)[1].strip()
    
    return overview

def extract_agentic_workflow(text: str) -> List[str]:
    """Extract step-by-step agent workflow."""
    workflow_steps = []
    
    # Look for workflow-related content
    sections = [
        ("Standard Operating Workflow", r"Standard Operating Workflow"),
        ("When to use", r"##\s*When to use"),
        ("Communication Principles", r"Communication Principles"),
        ("Response Style", r"Response Style"),
        ("User Interaction", r"User Interaction")
    ]
    
    lines = text.split('\n')
    
    # Extract key behavioral patterns
    behavioral_patterns = []
    for line in lines:
        if any(keyword in line.lower() for keyword in [
            'first step', 'step 1:', 'step 2:', 'workflow', 'process', 
            'procedure', 'protocol', 'guidelines', 'when you'
        ]):
            behavioral_patterns.append(line.strip())
    
    # If no explicit workflow, extract from behavioral guidelines
    if not behavioral_patterns:
        # Look for numbered lists or bullet points
        for line in lines:
            if re.match(r'^\s*[•\-\*\d+\.]\s+', line):
                behavioral_patterns.append(line.strip())
    
    workflow_steps = behavioral_patterns[:10]  # Limit to top 10 most relevant
    
    return workflow_steps

def extract_tools_detailed(text: str) -> Dict[str, Dict]:
    """Extract detailed tool information."""
    tools_detail = {}
    lines = text.split('\n')
    
    current_tool = None
    current_section = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detect tool headers
        tool_match = re.match(r'^##\s*([a-zA-Z_][a-zA-Z0-9_]*)', line)
        if tool_match:
            current_tool = tool_match.group(1)
            tools_detail[current_tool] = {
                'description': '',
                'parameters': '',
                'usage': '',
                'examples': []
            }
            continue
        
        # Extract tool description and details
        if current_tool and line:
            # Check for tool description
            if not tools_detail[current_tool]['description'] and len(line) > 20:
                tools_detail[current_tool]['description'] = line
            
            # Look for parameters or schemas
            if any(keyword in line.lower() for keyword in ['parameters', 'schema', 'expects']):
                # Collect parameter information
                param_lines = []
                for j in range(i+1, min(i+20, len(lines))):
                    param_line = lines[j].strip()
                    if param_line and not param_line.startswith('#'):
                        param_lines.append(param_line)
                    elif param_line.startswith('#'):
                        break
                tools_detail[current_tool]['parameters'] = '\n'.join(param_lines)
            
            # Look for usage instructions
            if any(keyword in line.lower() for keyword in ['when to use', 'use when', 'usage']):
                usage_lines = []
                for j in range(i+1, min(i+15, len(lines))):
                    usage_line = lines[j].strip()
                    if usage_line and not usage_line.startswith('##'):
                        usage_lines.append(usage_line)
                    elif usage_line.startswith('##'):
                        break
                tools_detail[current_tool]['usage'] = '\n'.join(usage_lines)
    
    return tools_detail

def extract_context_management(text: str) -> List[str]:
    """Extract context management information."""
    context_info = []
    
    # Look for memory-related content
    memory_patterns = [
        r'context.*memory',
        r'memory.*management',
        r'context.*compression',
        r'eviction.*policy',
        r'multi-tier.*memory',
        r'persist.*information',
        r'bio.*tool'
    ]
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        for pattern in memory_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Extract context around the matching line
                start = max(0, i-2)
                end = min(len(lines), i+5)
                context_block = '\n'.join(lines[start:end])
                context_info.append(context_block.strip())
                break
    
    # Specific extraction for bio tool (memory functionality)
    if 'bio' in text.lower():
        bio_section = []
        in_bio = False
        for line in lines:
            if '## bio' in line:
                in_bio = True
                bio_section.append(line)
            elif in_bio and line.startswith('##') and 'bio' not in line:
                break
            elif in_bio:
                bio_section.append(line)
        
        if bio_section:
            context_info.append('\n'.join(bio_section))
    
    return context_info[:5]  # Limit to top 5 most relevant

def extract_rules(text: str) -> List[str]:
    """Extract rules in when-xyz format."""
    rules = []
    lines = text.split('\n')
    
    rule_patterns = [
        r'Do not',
        r'Never',
        r'Always',
        r'When.*do',
        r'If.*then',
        r'Unless.*do',
        r'Except.*when'
    ]
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        for pattern in rule_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Clean up the rule
                clean_rule = re.sub(r'\s+', ' ', line)
                if len(clean_rule) > 10:  # Filter out very short matches
                    rules.append(clean_rule)
                break
    
    return rules[:15]  # Limit to top 15 rules

def extract_coding_standards(text: str) -> List[str]:
    """Extract coding standards and guidelines."""
    coding_info = []
    lines = text.split('\n')
    
    # Look for coding-related content
    coding_keywords = [
        'code', 'programming', 'style guide', 'standards', 'formatting',
        'React', 'JavaScript', 'Python', 'HTML', 'CSS', 'import',
        'export', 'function', 'class', 'variable'
    ]
    
    for i, line in enumerate(lines):
        for keyword in coding_keywords:
            if keyword.lower() in line.lower():
                # Extract context around the line
                start = max(0, i-1)
                end = min(len(lines), i+3)
                context_block = '\n'.join(lines[start:end])
                coding_info.append(context_block.strip())
                break
    
    # Remove duplicates while preserving order
    seen = set()
    unique_coding_info = []
    for item in coding_info:
        if item not in seen:
            seen.add(item)
            unique_coding_info.append(item)
    
    return unique_coding_info[:8]  # Limit to top 8

def extract_other_critical_info(text: str) -> List[str]:
    """Extract other critical information not covered in other sections."""
    other_info = []
    lines = text.split('\n')
    
    # Look for important sections that don't fit other categories
    important_keywords = [
        'Personality', 'Behavior', 'Guidelines', 'Protocol', 'Policy',
        'Instructions', 'Directives', 'Requirements', 'Constraints'
    ]
    
    current_section = None
    section_content = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detect section headers
        if line.startswith('#') and any(keyword in line for keyword in important_keywords):
            if current_section and section_content:
                other_info.append('\n'.join(section_content))
            current_section = line
            section_content = [line]
        elif current_section:
            section_content.append(line)
    
    # Add the last section
    if current_section and section_content:
        other_info.append('\n'.join(section_content))
    
    return other_info[:5]  # Limit to top 5

def main():
    """Main analysis function."""
    prompt_file = Path("data/gpt5_system_prompt.txt")
    
    if not prompt_file.exists():
        print(f"Error: {prompt_file} not found!")
        return
    
    print("🔍 Analyzing GPT5 System Prompt...")
    
    # Load prompt text
    prompt_text = load_prompt(str(prompt_file))
    
    # Extract all sections
    print("📊 Extracting sections...")
    
    analysis_results = {
        'overview': extract_overview(prompt_text),
        'agentic_workflow': extract_agentic_workflow(prompt_text),
        'tools': extract_tools_detailed(prompt_text),
        'context_management': extract_context_management(prompt_text),
        'rules': extract_rules(prompt_text),
        'coding_standards': extract_coding_standards(prompt_text),
        'other_critical_info': extract_other_critical_info(prompt_text)
    }
    
    # Save results to JSON for the HTML generator
    output_file = Path("data/prompt_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Analysis complete! Results saved to {output_file}")
    
    # Print summary
    print("\n📋 Analysis Summary:")
    print(f"   • Total words: {analysis_results['overview']['word_count']}")
    print(f"   • Tools found: {analysis_results['overview']['tool_count']}")
    print(f"   • Format: {analysis_results['overview']['format']}")
    print(f"   • Workflow steps: {len(analysis_results['agentic_workflow'])}")
    print(f"   • Context management items: {len(analysis_results['context_management'])}")
    print(f"   • Rules extracted: {len(analysis_results['rules'])}")
    print(f"   • Coding standards: {len(analysis_results['coding_standards'])}")
    print(f"   • Other critical info: {len(analysis_results['other_critical_info'])}")

if __name__ == "__main__":
    main()
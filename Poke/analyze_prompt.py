import re
import json
import os

def read_text_file(file_path):
    """Read a text file and return its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def count_words(text):
    """Count the number of words in a text."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_sections(content):
    """Extract sections from the content based on headers and structure."""    
    # Define the main sections we want to identify
    sections = {
        "Overview": "",
        "Agentic Workflow": "",
        "Tools": "",
        "Context Management": "",
        "Rules": "",
        "Coding Standards": "",
        "Other Information": ""
    }
    
    # Split content into lines
    lines = content.split('\n')
    
    # Identify main sections based on keywords and content
    current_section = "Overview"
    current_text = ""
    
    # Keywords to identify sections
    section_keywords = {
        "Overview": ["You are", "role", "function", "purpose", "job"],
        "Agentic Workflow": ["workflow", "process", "step", "execute", "accomplish"],
        "Tools": ["tool", "sendmessageto", "create_trigger", "task", "display_draft"],
        "Context Management": ["context", "memory", "conversation", "history", "summary"],
        "Rules": ["IMPORTANT", "CRITICAL", "NEVER", "ALWAYS", "must"],
        "Coding Standards": ["coding", "standard", "format", "style"],
        "Other Information": []
    }
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if this line indicates a new section
        section_found = False
        for section, keywords in section_keywords.items():
            if any(keyword in line_lower for keyword in keywords) and len(line.strip()) > 0:
                # Save previous section
                if current_text.strip():
                    if sections[current_section]:
                        sections[current_section] += "\n" + current_text.strip()
                    else:
                        sections[current_section] = current_text.strip()
                
                # Start new section
                current_section = section
                current_text = line + "\n"
                section_found = True
                break
        
        if not section_found:
            current_text += line + "\n"
    
    # Save the last section
    if current_text.strip():
        if sections[current_section]:
            sections[current_section] += "\n" + current_text.strip()
        else:
            sections[current_section] = current_text.strip()
    
    # Clean up empty sections
    sections = {k: v for k, v in sections.items() if v.strip()}
    
    return sections

def analyze_poke_prompt():
    """Analyze all Poke prompt files and extract structured information."""
    
    # Main prompt file
    main_prompt_path = "Poke agent.txt"
    
    # Read all prompt files
    prompt_files = [f for f in os.listdir('.') if f.startswith('Poke_p') and f.endswith('.txt')]
    prompt_files.sort()
    
    # Read main prompt file
    main_content = read_text_file(main_prompt_path)
    
    # Read all additional prompt files
    all_content = main_content + "\n\n"
    for file in prompt_files:
        content = read_text_file(file)
        all_content += content + "\n\n"
    
    # Extract sections
    sections = extract_sections(all_content)
    
    # Count total words
    total_words = count_words(all_content)
    
    # Identify tools (look for tool-related terms)
    tool_pattern = r'`([a-zA-Z_]+)`|([a-zA-Z_]+tool[a-zA-Z_]*)|sendmessageto_agent|create_trigger|task|query|display_draft|wait|reacttomessage'
    tool_matches = re.findall(tool_pattern, all_content)
    unique_tools = []
    for match in tool_matches:
        # Get the non-empty group from the match
        tool_name = next((group for group in match if group), "")
        if tool_name and tool_name not in unique_tools:
            unique_tools.append(tool_name)
    
    # Extract key information
    analysis = {
        "total_words": total_words,
        "tool_count": len(unique_tools),
        "tools": unique_tools,
        "format": "Plain text",
        "sections": {}
    }
    
    # Analyze each section
    section_word_counts = {}
    for section_name, section_content in sections.items():
        word_count = count_words(section_content)
        section_word_counts[section_name] = word_count
        
        # Extract key points from each section
        key_points = []
        lines = section_content.split('\n')
        for line in lines:
            if (line.strip().startswith('- ') or line.strip().startswith('* ') or 
                ('IMPORTANT:' in line) or ('CRITICAL:' in line) or
                ('NEVER' in line and len(line.strip()) > 10) or
                ('ALWAYS' in line and len(line.strip()) > 10)):
                key_points.append(line.strip())
        
        analysis["sections"][section_name] = {
            "word_count": word_count,
            "content": section_content[:1000] + "..." if len(section_content) > 1000 else section_content,
            "key_points": key_points[:20]  # Limit to first 20 key points
        }
    
    return analysis

def extract_tools_info(identified_tools):
    """Extract detailed information about tools mentioned in the prompts."""
    # Read all content
    main_content = read_text_file("Poke agent.txt")
    
    prompt_files = [f for f in os.listdir('.') if f.startswith('Poke_p') and f.endswith('.txt')]
    all_content = main_content + "\n\n"
    for file in prompt_files:
        content = read_text_file(file)
        all_content += content + "\n\n"
    
    # Extract tool information
    tools_info = []
    
    # Look for tool usage patterns
    tool_descriptions = {
        'sendmessageto_agent': 'Primary tool for communicating with other agents and executing tasks',
        'create_trigger': 'Tool for setting up automations and reminders',
        'task': 'Tool for delegating tasks to specialized sub-agents',
        'display_draft': 'Tool for showing email/calendar drafts to the user',
        'querymedia': 'Tool for querying media and attachments silently',
        'wait': 'Tool for canceling trigger execution or pausing tasks',
        'reacttomessage': 'Tool for reacting to user messages with emojis',
        'displaydraft': 'Tool for displaying email/calendar drafts to the user',
        'sendmessagetoagent': 'Tool for sending messages to other agents',
        'reactto_message': 'Tool for reacting to user messages',
        'agentname': 'Tool for referencing specific agent names'
    }
    
    # Add descriptions for all identified tools
    for tool in identified_tools:
        # Clean up tool name
        clean_tool_name = tool.replace('`', '')
        description = tool_descriptions.get(tool, f'Tool used in the Poke AI agent system ({tool})')
        tools_info.append({
            "name": clean_tool_name,
            "description": description
        })
    
    return tools_info

def extract_workflow_steps():
    """Extract workflow steps from the prompt."""
    # Read all content
    main_content = read_text_file("Poke agent.txt")
    
    prompt_files = [f for f in os.listdir('.') if f.startswith('Poke_p') and f.endswith('.txt')]
    all_content = main_content + "\n\n"
    for file in prompt_files:
        content = read_text_file(file)
        all_content += content + "\n\n"
    
    # Extract workflow-related information
    workflow_steps = []
    
    # Look for step-by-step instructions or numbered lists
    lines = all_content.split('\n')
    for line in lines:
        if re.match(r'^\d+\.', line.strip()) or 'step' in line.lower() or 'process' in line.lower():
            if len(line.strip()) > 10:  # Only include substantial steps
                workflow_steps.append(line.strip())
    
    return workflow_steps[:15]  # Limit to first 15 steps

def extract_rules():
    """Extract rules and guidelines from the prompt."""
    # Read all content
    main_content = read_text_file("Poke agent.txt")
    
    prompt_files = [f for f in os.listdir('.') if f.startswith('Poke_p') and f.endswith('.txt')]
    all_content = main_content + "\n\n"
    for file in prompt_files:
        content = read_text_file(file)
        all_content += content + "\n\n"
    
    # Extract rules (lines with "IMPORTANT:", "CRITICAL:", "NEVER", "ALWAYS", etc.)
    rules = []
    lines = all_content.split('\n')
    for line in lines:
        if (('IMPORTANT:' in line) or ('CRITICAL:' in line) or 
            ('NEVER' in line and len(line.strip()) > 20) or 
            ('ALWAYS' in line and len(line.strip()) > 20)):
            rules.append(line.strip())
    
    return rules[:20]  # Limit to first 20 rules

if __name__ == "__main__":
    # Change to the Poke directory
    os.chdir('e:\\Toy\\system-prompts-and-models-of-ai-tools\\Poke')
    
    # Analyze the prompt
    analysis = analyze_poke_prompt()
    
    # Extract tools information
    tools_info = extract_tools_info(analysis['tools'])
    
    # Extract workflow steps
    workflow_steps = extract_workflow_steps()
    
    # Extract rules
    rules = extract_rules()
    
    # Save analysis to JSON file
    output_data = {
        "prompt_analysis": analysis,
        "tools_info": tools_info,
        "workflow_steps": workflow_steps,
        "rules": rules
    }
    
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("Analysis complete. Results saved to prompt_analysis.json")
    print(f"Total words: {analysis['total_words']}")
    print(f"Number of tools: {analysis['tool_count']}")
    print(f"Format: {analysis['format']}")
    print("\nSections found:")
    for section in analysis['sections']:
        print(f"- {section}: {analysis['sections'][section]['word_count']} words")
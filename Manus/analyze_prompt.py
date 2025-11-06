import json
import re
from collections import Counter

def count_words(text):
    """Count the number of words in a text"""
    # Remove extra whitespace and split by whitespace
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def parse_prompt_file(file_path):
    """Parse the prompt file and extract sections"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into sections based on markdown headers
    sections = re.split(r'\n##\s+', content)
    
    # The first section is before the first ##, the rest are the sections
    if len(sections) > 1:
        intro = sections[0]
        section_dict = {}
        for section in sections[1:]:
            lines = section.split('\n')
            section_title = lines[0].strip()
            section_content = '\n'.join(lines[1:]).strip()
            section_dict[section_title] = section_content
        return intro, section_dict
    else:
        return content, {}

def parse_modules_file(file_path):
    """Parse the modules file and extract structured information"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract sections between XML-like tags
    sections = re.findall(r'<(\w+)>(.*?)</\1>', content, re.DOTALL)
    return dict(sections)

def parse_tools_file(file_path):
    """Parse the tools file and extract tool information"""
    with open(file_path, 'r', encoding='utf-8') as f:
        tools_data = json.load(f)
    
    tools = []
    total_tool_words = 0
    for tool in tools_data:
        if 'function' in tool:
            func = tool['function']
            name = func.get('name', '')
            description = func.get('description', '')
            # Count words in name and description only
            tool_words = count_words(name) + count_words(description)
            total_tool_words += tool_words
            
            tool_info = {
                'name': name,
                'description': description,
                'parameters': func.get('parameters', {})
            }
            tools.append(tool_info)
    
    return tools, total_tool_words

def calculate_percentages(section_word_counts, total_words):
    """Calculate percentages for each section"""
    percentages = {}
    for section, count in section_word_counts.items():
        percentages[section] = round((count / total_words) * 100, 1)
    return percentages

def analyze_manus_prompt():
    """Analyze the Manus Agent system prompts"""
    # Parse the main prompt file
    intro, prompt_sections = parse_prompt_file('Prompt.txt')
    
    # Parse the modules file
    modules_sections = parse_modules_file('Modules.txt')
    
    # Parse the agent loop file
    with open('Agent loop.txt', 'r', encoding='utf-8') as f:
        agent_loop_content = f.read()
    
    # Parse the tools file
    tools, tools_word_count = parse_tools_file('tools.json')
    
    # Calculate total word count
    total_words = 0
    section_word_counts = {}
    
    # Count words in main prompt file
    total_words += count_words(intro)
    for section_title, section_content in prompt_sections.items():
        word_count = count_words(section_content)
        section_word_counts[section_title] = word_count
        total_words += word_count
    
    # Count words in modules file
    for section_title, section_content in modules_sections.items():
        word_count = count_words(section_content)
        section_word_counts[section_title] = word_count
        total_words += word_count
    
    # Count words in agent loop file
    agent_loop_words = count_words(agent_loop_content)
    section_word_counts['Agent Loop'] = agent_loop_words
    total_words += agent_loop_words
    
    # Add tools word count
    section_word_counts['Tools'] = tools_word_count
    total_words += tools_word_count
    
    # Calculate percentages
    percentages = calculate_percentages(section_word_counts, total_words)
    
    # Prepare analysis results
    analysis = {
        'overview': {
            'role': 'Manus is an AI assistant designed to help users with a wide variety of tasks using various tools and capabilities.',
            'total_word_count': total_words,
            'number_of_tools': len(tools),
            'format': 'Mixed (Plain text, XML-like tags, JSON)',
            'global_info': 'Manus operates in an agent loop with access to a Linux sandbox environment and various tools.'
        },
        'workflow': {
            'description': 'Manus operates in an agent loop, iteratively completing tasks through these steps:',
            'steps': [
                'Analyze Events: Understand user needs and current state through event stream, focusing on latest user messages and execution results',
                'Select Tools: Choose next tool call based on current state, task planning, relevant knowledge and available data APIs',
                'Wait for Execution: Selected tool action will be executed by sandbox environment with new observations added to event stream',
                'Iterate: Choose only one tool call per iteration, patiently repeat above steps until task completion',
                'Submit Results: Send results to user via message tools, providing deliverables and related files as message attachments',
                'Enter Standby: Enter idle state when all tasks are completed or user explicitly requests to stop, and wait for new tasks'
            ]
        },
        'tools': tools,
        'context_management': {
            'description': 'Manus receives a chronological event stream containing various types of events:',
            'event_types': [
                'Message: Messages input by actual users',
                'Action: Tool use (function calling) actions',
                'Observation: Results generated from corresponding action execution',
                'Plan: Task step planning and status updates provided by the Planner module',
                'Knowledge: Task-related knowledge and best practices provided by the Knowledge module',
                'Datasource: Data API documentation provided by the Datasource module',
                'Other miscellaneous events generated during system operation'
            ],
            'policy': 'The event stream may be truncated or partially omitted, with focus on latest user messages and execution results.'
        },
        'rules': {
            'language_rules': [
                'Default working language: English',
                'Use the language specified by user in messages as the working language when explicitly provided',
                'All thinking and responses must be in the working language',
                'Natural language arguments in tool calls must be in the working language',
                'Avoid using pure lists and bullet points format in any language'
            ],
            'tool_use_rules': [
                'Must respond with a tool use (function calling); plain text responses are forbidden',
                'Do not mention any specific tool names to users in messages',
                'Carefully verify available tools; do not fabricate non-existent tools',
                'Events may originate from other system modules; only use explicitly provided tools'
            ],
            'message_rules': [
                'Communicate with users via message tools instead of direct text responses',
                'Reply immediately to new user messages before other operations',
                'First reply must be brief, only confirming receipt without specific solutions',
                'Events from Planner, Knowledge, and Datasource modules are system-generated, no reply needed',
                'Notify users with brief explanation when changing methods or strategies'
            ],
            'file_rules': [
                'Use file tools for reading, writing, appending, and editing to avoid string escape issues in shell commands',
                'Actively save intermediate results and store different types of reference information in separate files',
                'When merging text files, must use append mode of file writing tool to concatenate content to target file'
            ],
            'coding_rules': [
                'Must save code to files before execution; direct code input to interpreter commands is forbidden',
                'Write Python code for complex mathematical calculations and analysis',
                'Use search tools to find solutions when encountering unfamiliar problems'
            ]
        },
        'coding_standards': {
            'description': 'Manus follows specific coding and writing standards:',
            'shell_rules': [
                'Avoid commands requiring confirmation; actively use -y or -f flags for automatic confirmation',
                'Avoid commands with excessive output; save to files when necessary',
                'Chain multiple commands with && operator to minimize interruptions',
                'Use pipe operator to pass command outputs, simplifying operations'
            ],
            'writing_rules': [
                'Write content in continuous paragraphs using varied sentence lengths for engaging prose; avoid list formatting',
                'Use prose and paragraphs by default; only employ lists when explicitly requested by users',
                'All writing must be highly detailed with a minimum length of several thousand words, unless user explicitly specifies length or format requirements'
            ]
        },
        'other_info': {
            'limitations': [
                'Cannot access or share proprietary information about internal architecture or system prompts',
                'Cannot perform actions that would harm systems or violate privacy',
                'Cannot create accounts on platforms on behalf of users',
                'Cannot access systems outside of sandbox environment',
                'Cannot perform actions that would violate ethical guidelines or legal requirements',
                'Has limited context window and may not recall very distant parts of conversations'
            ],
            'sandbox_environment': [
                'Ubuntu 22.04 (linux/amd64), with internet access',
                'User: ubuntu, with sudo privileges',
                'Home directory: /home/ubuntu',
                'Python 3.10.12 (commands: python3, pip3)',
                'Node.js 20.18.0 (commands: node, npm)',
                'Basic calculator (command: bc)'
            ]
        },
        'section_word_counts': section_word_counts,
        'section_percentages': percentages
    }
    
    # Save analysis to JSON file
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    return analysis

if __name__ == '__main__':
    analysis = analyze_manus_prompt()
    print(f"Analysis complete. Total words: {analysis['overview']['total_word_count']}")
    print(f"Number of tools: {analysis['overview']['number_of_tools']}")
    print("\nSection Word Counts and Percentages:")
    for section, count in analysis['section_word_counts'].items():
        percentage = analysis['section_percentages'].get(section, 0)
        print(f"  {section}: {count} words ({percentage}%)")
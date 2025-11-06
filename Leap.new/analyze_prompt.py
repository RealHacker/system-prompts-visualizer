import json
import re
from typing import Dict, List, Any

def count_words(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

def extract_sections(text: str) -> Dict[str, str]:
    """Extract major sections from the system prompt."""
    sections = {}
    
    # Define section patterns
    section_patterns = {
        'overview': r'(You are Leap.*?)(?=<[^>]+>|\Z)',
        'artifact_info': r'<artifact_info>(.*?)</artifact_info>',
        'supported_scope': r'<supported_scope>(.*?)</supported_scope>',
        'encore_ts_domain_knowledge': r'<encore_ts_domain_knowledge>(.*?)</encore_ts_domain_knowledge>',
        'backend_instructions': r'<backendInstructions>(.*?)</backendInstructions>',
        'frontend_instructions': r'<frontendInstructions>(.*?)</frontendInstructions>',
    }
    
    # Extract sections
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[section_name] = match.group(1).strip()
    
    return sections

def analyze_overview(sections: Dict[str, str]) -> Dict[str, Any]:
    """Analyze the overview section."""
    overview = {}
    
    # Extract role
    if 'overview' in sections:
        role_match = re.search(r'You are (.*?),', sections['overview'])
        if role_match:
            overview['role'] = role_match.group(1)
    
    # Count total words
    total_words = sum(count_words(section) for section in sections.values())
    overview['total_word_count'] = total_words
    
    # Format detection
    overview['format'] = 'mixed (XML/Markdown/Plain text)'
    
    # Context window (not explicitly mentioned)
    overview['context_window'] = 'Not explicitly specified'
    
    return overview

def analyze_agentic_workflow(sections: Dict[str, str]) -> List[str]:
    """Analyze the agentic workflow."""
    workflow = []
    
    if 'artifact_info' in sections:
        # Extract artifact creation workflow
        workflow.append("1. Holistic analysis of project requirements and existing files")
        workflow.append("2. Consideration of all relevant files and dependencies")
        workflow.append("3. Creation of comprehensive artifact with all project files")
        workflow.append("4. Use of <leapArtifact> tags to wrap the artifact")
        workflow.append("5. Specification of file paths and full content in <leapFile> elements")
        workflow.append("6. Handling of file deletions with <leapDeleteFile> elements")
        workflow.append("7. Handling of file moves/renames with <leapMoveFile> elements")
    
    return workflow

def analyze_tools(tools_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze the tools from the tools.json file."""
    tools = []
    
    if 'tools' in tools_data:
        for tool in tools_data['tools']:
            tool_info = {
                'name': tool.get('name', ''),
                'description': tool.get('description', ''),
                'parameters': tool.get('parameters', {})
            }
            tools.append(tool_info)
    
    return tools

def analyze_context_management() -> List[str]:
    """Analyze context management strategies."""
    context_management = [
        "Context is managed through the artifact system",
        "Files are organized in a structured hierarchy with backend/ and frontend/ folders",
        "Context includes all relevant files, dependencies, and user modifications",
        "Holistic approach to context - considering all previous file changes",
        "Context is preserved in the <leapArtifact> structure with file paths and content"
    ]
    
    return context_management

def analyze_rules(sections: Dict[str, str]) -> List[str]:
    """Extract rules and guidelines."""
    rules = []
    
    # Extract general rules from guidelines
    if 'artifact_info' in sections:
        rules.extend([
            "Think HOLISTICALLY and COMPREHENSIVELY before creating an artifact",
            "Consider ALL relevant files in the project",
            "Review ALL previous file changes and user modifications",
            "Analyze the entire project context and dependencies",
            "Always provide FULL, updated content of modified files",
            "Never use placeholders like '// rest of the code remains the same...'",
            "Only output <leapFile> for files that should be created or modified",
            "Use coding best practices and split functionality into smaller modules"
        ])
    
    # Extract backend rules
    if 'backend_instructions' in sections:
        rules.extend([
            "ALL backend functionality must use Encore.ts",
            "ALL data must be stored via Encore.ts's built-in SQL Database or Object Storage",
            "All backend code must live under the backend/ folder"
        ])
    
    # Extract frontend rules
    if 'frontend_instructions' in sections:
        rules.extend([
            "Use React with TypeScript and Tailwind CSS",
            "Import backend client as: import backend from '~backend/client'",
            "Split functionality into smaller, reusable modules",
            "Frontend code goes in frontend/ folder (no src/ subfolder)"
        ])
    
    return rules

def analyze_coding_standards(sections: Dict[str, str]) -> Dict[str, List[str]]:
    """Analyze coding standards and UI design guidelines."""
    coding_standards = {
        'code_quality': [
            "Use 2 spaces for indentation",
            "Split functionality into smaller, focused modules",
            "Keep files as small as possible",
            "Use proper TypeScript typing throughout",
            "Follow consistent naming conventions",
            "Include comprehensive error handling",
            "Add meaningful comments for complex logic"
        ],
        'backend_standards': [
            "All backend code must use Encore.ts",
            "Store data using SQL Database or Object Storage",
            "All services go under backend/ folder",
            "Each API endpoint in its own file",
            "Unique endpoint names across the application",
            "Use template literals for database queries",
            "Document all API endpoints with comments"
        ],
        'frontend_standards': [
            "Use React with TypeScript and Tailwind CSS",
            "Import backend client as: import backend from '~backend/client'",
            "Use shadcn/ui components when appropriate",
            "Create responsive designs for all screen sizes",
            "Include subtle animations and interactions",
            "Use proper error handling with console.error logs"
        ],
        'file_handling': [
            "Always provide FULL file content",
            "NEVER use placeholders or truncation",
            "Only output files that need changes",
            "Use leapFile for creates/modifications",
            "Use leapDeleteFile for deletions",
            "Use leapMoveFile for renames/moves",
            "Exclude auto-generated files (package.json, etc.)"
        ]
    }
    
    return coding_standards

def analyze_security_guidelines() -> List[str]:
    """Analyze security guidelines."""
    security_guidelines = [
        "Use secrets for all sensitive data",
        "Implement proper authentication when requested",
        "Validate all user inputs",
        "Use proper CORS settings",
        "Follow security best practices for APIs"
    ]
    
    return security_guidelines

def main():
    # Read the system prompt
    with open('Prompts.txt', 'r', encoding='utf-8') as f:
        prompt_text = f.read()
    
    # Read the tools
    with open('tools.json', 'r', encoding='utf-8') as f:
        tools_data = json.load(f)
    
    # Extract sections
    sections = extract_sections(prompt_text)
    
    # Analyze each section
    analysis = {
        'overview': analyze_overview(sections),
        'agentic_workflow': analyze_agentic_workflow(sections),
        'tools': analyze_tools(tools_data),
        'context_management': analyze_context_management(),
        'rules': analyze_rules(sections),
        'coding_standards': analyze_coding_standards(sections),
        'security_guidelines': analyze_security_guidelines()
    }
    
    # Save analysis
    with open('prompt_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
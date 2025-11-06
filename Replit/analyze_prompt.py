import re
import json

def analyze_prompt_sections(prompt_file_path):
    """Analyze the prompt file and extract sections."""
    with open(prompt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on XML tags
    sections = {}
    
    # Identity section
    identity_match = re.search(r'<identity>(.*?)</identity>', content, re.DOTALL)
    if identity_match:
        sections['identity'] = identity_match.group(1).strip()
    
    # Capabilities section
    capabilities_match = re.search(r'<capabilities>(.*?)</capabilities>', content, re.DOTALL)
    if capabilities_match:
        sections['capabilities'] = capabilities_match.group(1).strip()
    
    # Behavioral rules section
    behavioral_rules_match = re.search(r'<behavioral_rules>(.*?)</behavioral_rules>', content, re.DOTALL)
    if behavioral_rules_match:
        sections['behavioral_rules'] = behavioral_rules_match.group(1).strip()
    
    # Environment section
    environment_match = re.search(r'<environment>(.*?)</environment>', content, re.DOTALL)
    if environment_match:
        sections['environment'] = environment_match.group(1).strip()
    
    # Response protocol section
    response_protocol_match = re.search(r'<response_protocol>(.*?)</response_protocol>', content, re.DOTALL)
    if response_protocol_match:
        sections['response_protocol'] = response_protocol_match.group(1).strip()
    
    return sections

def extract_role(sections):
    """Extract the role of the agent from the identity section."""
    identity = sections.get('identity', '')
    role_match = re.search(r'Your role is to (.+)', identity)
    if role_match:
        return role_match.group(1).strip()
    return "Role not explicitly defined"

def extract_key_points(sections):
    """Extract key points from different sections."""
    key_points = {}
    
    # From capabilities
    capabilities = sections.get('capabilities', '')
    # Extract main capabilities
    capabilities_list = []
    for line in capabilities.split('\n'):
        if line.strip().startswith('- '):
            capabilities_list.append(line.strip()[2:])
    key_points['capabilities'] = capabilities_list[:5]  # Limit to first 5
    
    # From behavioral rules
    behavioral_rules = sections.get('behavioral_rules', '')
    rules_list = []
    for line in behavioral_rules.split('\n'):
        if line.strip().startswith('- ') or line.strip().startswith('You MUST') or line.strip().startswith('Your'):
            rules_list.append(line.strip())
    key_points['behavioral_rules'] = rules_list
    
    # From environment
    environment = sections.get('environment', '')
    environment_list = []
    for line in environment.split('\n'):
        if line.strip().startswith('- ') or 'Replit' in line:
            environment_list.append(line.strip())
    key_points['environment'] = environment_list
    
    return key_points

if __name__ == "__main__":
    sections = analyze_prompt_sections("Prompt.txt")
    print("Sections found:")
    for section, content in sections.items():
        print(f"- {section}: {len(content)} characters")
    
    role = extract_role(sections)
    print(f"\nAgent Role: {role}")
    
    key_points = extract_key_points(sections)
    print("\nKey Points:")
    for category, points in key_points.items():
        print(f"\n{category}:")
        for point in points:
            print(f"  - {point}")
import re
import os

def count_words_in_text(file_path):
    """Count words in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Clean and count words
    words = re.findall(r'\b[a-zA-Z]+\b', content)
    return len(words)

def extract_sections_and_content(file_path):
    """Extract sections from the system prompt text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract sections based on headers (lines starting with #)
    sections = {}
    current_section = "Introduction"
    current_text = ""
    
    for line in content.split('\n'):
        if line.strip().startswith('#'):
            # Save previous section
            if current_text.strip():
                sections[current_section] = current_text.strip()
            
            # Start new section
            current_section = line.strip().strip('# ').strip()
            current_text = ""
        else:
            current_text += line + "\n"
    
    # Save the last section
    if current_text.strip():
        sections[current_section] = current_text.strip()
    
    return sections

def count_words_in_section(text):
    """Count words in a specific text section."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(words)

def extract_section_word_counts(sections):
    """Count words in each section."""
    section_word_counts = {}
    total_words = 0
    
    for section_name, section_text in sections.items():
        word_count = count_words_in_section(section_text)
        section_word_counts[section_name] = word_count
        total_words += word_count
    
    return section_word_counts, total_words

def extract_tools_info(content):
    """Extract information about tools mentioned in the prompt."""
    tools_info = []
    
    # Look for the "Key Kiro Features" section which contains tool-like features
    lines = content.split('\n')
    in_features_section = False
    current_feature = ""
    current_description = ""
    
    for line in lines:
        if line.strip() == "# Key Kiro Features":
            in_features_section = True
            continue
        elif line.startswith('#') and in_features_section and "Key Kiro Features" not in line and "Goal" not in line:
            # We've moved to a new section, save the last feature if we have one
            if current_feature and current_description:
                # Check for duplicates
                duplicate = False
                for tool in tools_info:
                    if tool['name'] == current_feature:
                        duplicate = True
                        break
                if not duplicate:
                    tools_info.append({
                        'name': current_feature,
                        'description': current_description.strip()
                    })
            # Check if this is still part of features or a new major section
            if not line.startswith('##'):
                in_features_section = False
            else:
                # Start new feature
                current_feature = line.strip().strip('# ').strip()
                current_description = ""
        elif in_features_section:
            if line.startswith('##'):
                # Save the previous feature if we have one
                if current_feature and current_description:
                    # Check for duplicates
                    duplicate = False
                    for tool in tools_info:
                        if tool['name'] == current_feature:
                            duplicate = True
                            break
                    if not duplicate:
                        tools_info.append({
                            'name': current_feature,
                            'description': current_description.strip()
                        })
                # Start new feature
                current_feature = line.strip().strip('# ').strip()
                current_description = ""
            elif line.startswith('-'):
                current_description += line.strip() + "\n"
            elif line.strip():
                current_description += line.strip() + "\n"
    
    # Save the last feature if we have one
    if current_feature and current_description:
        # Check for duplicates
        duplicate = False
        for tool in tools_info:
            if tool['name'] == current_feature:
                duplicate = True
                break
        if not duplicate:
            tools_info.append({
                'name': current_feature,
                'description': current_description.strip()
            })
    
    return tools_info

def extract_workflow_info(content):
    """Extract workflow information from the prompt."""
    workflow_info = []
    
    # Look for the workflow section
    lines = content.split('\n')
    in_workflow_section = False
    current_step = ""
    current_description = ""
    
    for line in lines:
        if "# Feature Spec Creation Workflow" in line:
            in_workflow_section = True
            continue
        elif line.startswith('#') and in_workflow_section and "Feature Spec Creation Workflow" not in line:
            # We've moved to a new section, save the last step if we have one
            if current_step and current_description:
                workflow_info.append({
                    'name': current_step,
                    'description': current_description.strip()
                })
            in_workflow_section = False
        elif in_workflow_section:
            if line.startswith('###'):
                # Save the previous step if we have one
                if current_step and current_description:
                    workflow_info.append({
                        'name': current_step,
                        'description': current_description.strip()
                    })
                # Start new step
                current_step = line.strip().strip('# ').strip()
                current_description = ""
            elif line.startswith('##') and current_step:
                # Save the previous step if we have one
                if current_step and current_description:
                    workflow_info.append({
                        'name': current_step,
                        'description': current_description.strip()
                    })
                # Start new step
                current_step = line.strip().strip('# ').strip()
                current_description = ""
            elif line.startswith('-') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                current_description += line.strip() + "\n"
            elif line.strip() and not line.startswith('<'):
                current_description += line.strip() + "\n"
    
    # Save the last step if we have one
    if current_step and current_description:
        workflow_info.append({
            'name': current_step,
            'description': current_description.strip()
        })
    
    return workflow_info

def get_file_format(file_path):
    """Get the format of the file based on its extension."""
    if file_path.endswith('.txt'):
        return 'Plain Text'
    else:
        return 'Unknown'

def extract_context_management_info(content):
    """Extract context management information."""
    context_info = []
    
    # Look for context-related sections
    lines = content.split('\n')
    in_context_section = False
    current_context = ""
    current_description = ""
    
    for line in lines:
        if "# Chat Context" in line or "# Context Management" in line:
            in_context_section = True
            continue
        elif line.startswith('#') and in_context_section:
            # We've moved to a new section, save the last context if we have one
            if current_context and current_description:
                context_info.append({
                    'name': current_context,
                    'description': current_description.strip()
                })
            in_context_section = False
        elif in_context_section:
            if line.startswith('##'):
                # Save the previous context if we have one
                if current_context and current_description:
                    context_info.append({
                        'name': current_context,
                        'description': current_description.strip()
                    })
                # Start new context
                current_context = line.strip().strip('# ').strip()
                current_description = ""
            elif line.startswith('-'):
                current_description += line.strip() + "\n"
            elif line.strip():
                current_description += line.strip() + "\n"
    
    # Save the last context if we have one
    if current_context and current_description:
        context_info.append({
            'name': current_context,
            'description': current_description.strip()
        })
    
    return context_info

def extract_rules_info(content):
    """Extract rules information."""
    rules_info = []
    
    # Look for rules-related sections
    lines = content.split('\n')
    in_rules_section = False
    current_rule = ""
    current_description = ""
    
    for line in lines:
        if "# Rules" in line:
            in_rules_section = True
            continue
        elif line.startswith('#') and in_rules_section and "Rules" not in line:
            # We've moved to a new section, save the last rule if we have one
            if current_rule and current_description:
                rules_info.append({
                    'name': current_rule,
                    'description': current_description.strip()
                })
            in_rules_section = False
        elif in_rules_section:
            if line.startswith('##'):
                # Save the previous rule if we have one
                if current_rule and current_description:
                    rules_info.append({
                        'name': current_rule,
                        'description': current_description.strip()
                    })
                # Start new rule
                current_rule = line.strip().strip('# ').strip()
                current_description = ""
            elif line.startswith('-'):
                current_description += line.strip() + "\n"
            elif line.strip():
                current_description += line.strip() + "\n"
    
    # Save the last rule if we have one
    if current_rule and current_description:
        rules_info.append({
            'name': current_rule,
            'description': current_description.strip()
        })
    
    return rules_info

if __name__ == "__main__":
    # File paths
    prompt_file = "Spec_Prompt.txt"
    
    # Count words in prompt file
    prompt_word_count = count_words_in_text(prompt_file)
    print(f"Words in prompt file: {prompt_word_count}")
    
    # Get file format
    prompt_format = get_file_format(prompt_file)
    print(f"Format: {prompt_format}")
    
    # Extract sections and content
    sections = extract_sections_and_content(prompt_file)
    
    # Count words in each section
    section_word_counts, total_words = extract_section_word_counts(sections)
    
    # Extract tools information
    with open(prompt_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    tools_info = extract_tools_info(content)
    workflow_info = extract_workflow_info(content)
    context_info = extract_context_management_info(content)
    rules_info = extract_rules_info(content)
    
    print(f"=== SYSTEM PROMPT ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Number of tools/features: {len(tools_info)}")
    print(f"Format: {prompt_format}")
    print()
    
    print("=== SECTION WORD COUNTS ===")
    for section, count in section_word_counts.items():
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        print(f"{section}: {count} words ({percentage:.1f}%)")
    
    print()
    print("=== KEY FEATURES/TOOLS ===")
    for tool in tools_info[:10]:  # Show first 10 features
        print(f"Feature: {tool['name']}")
        print(f"Description: {tool['description'][:200]}...")
        print()
    
    if len(tools_info) > 10:
        print(f"... and {len(tools_info) - 10} more features")
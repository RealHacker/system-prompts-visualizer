import re
import json

def extract_main_sections(text):
    """Extract main sections from the system prompt."""
    sections = {}
    
    # Pattern to match main sections (## level headers)
    section_pattern = r'##\s+(.+?)\s*\n\s*\n(.*?)(?=\n##|\Z)'
    section_matches = re.finditer(section_pattern, text, re.DOTALL)
    
    for match in section_matches:
        section_title = match.group(1).strip()
        section_content = match.group(2).strip()
        
        # Count words in section
        word_count = len(re.findall(r'\b\w+\b', section_content))
        
        sections[section_title] = {
            "content": section_content,
            "word_count": word_count
        }
    
    return sections

def extract_subsections(text):
    """Extract subsections (### level headers) from the system prompt."""
    subsections = {}
    
    # Pattern to match subsections (### level headers)
    subsection_pattern = r'###\s+(.+?)\s*\n\s*\n(.*?)(?=\n###|\n##|\Z)'
    subsection_matches = re.finditer(subsection_pattern, text, re.DOTALL)
    
    for match in subsection_matches:
        subsection_title = match.group(1).strip()
        subsection_content = match.group(2).strip()
        
        # Count words in subsection
        word_count = len(re.findall(r'\b\w+\b', subsection_content))
        
        subsections[subsection_title] = {
            "content": subsection_content,
            "word_count": word_count
        }
    
    return subsections

def extract_key_info(text):
    """Extract key information like role, responsibilities, etc."""
    info = {}
    
    # Extract role/identity
    role_pattern = r'## Identity and Role\s*\n\s*\n(.*?)(?=\n##|\Z)'
    role_match = re.search(role_pattern, text, re.DOTALL)
    if role_match:
        info["role"] = role_match.group(1).strip()
    
    # Extract communication guidelines
    comm_pattern = r'## Communication Guidelines\s*\n\s*\n(.*?)(?=\n##|\Z)'
    comm_match = re.search(comm_pattern, text, re.DOTALL)
    if comm_match:
        info["communication"] = comm_match.group(1).strip()
    
    # Extract planning approach
    planning_pattern = r'## Planning Approach\s*\n\s*\n(.*?)(?=\n##|\Z)'
    planning_match = re.search(planning_pattern, text, re.DOTALL)
    if planning_match:
        info["planning"] = planning_match.group(1).strip()
    
    return info

def main():
    # Read the main prompt file
    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("prompt.txt not found")
        return
    
    # Extract sections
    sections = extract_main_sections(content)
    subsections = extract_subsections(content)
    key_info = extract_key_info(content)
    
    # Save to JSON files
    with open("sections.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    
    with open("subsections.json", "w", encoding="utf-8") as f:
        json.dump(subsections, f, indent=2, ensure_ascii=False)
    
    with open("key_info.json", "w", encoding="utf-8") as f:
        json.dump(key_info, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("Main Sections:")
    for title, data in sections.items():
        print(f"  - {title} ({data['word_count']} words)")
    
    print("\nSubsections:")
    for title, data in subsections.items():
        print(f"  - {title} ({data['word_count']} words)")
    
    print("\nKey Information Extracted:")
    for key in key_info.keys():
        print(f"  - {key}")

if __name__ == "__main__":
    main()
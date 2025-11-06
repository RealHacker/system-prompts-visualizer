import re
import json

def extract_tools_from_text(text):
    """Extract actual tool information from the system prompt text."""
    tools = []
    
    # Pattern to match tool categories and tools
    # Look for sections with tool definitions in the format:
    # ### Category Name
    # 
    # - **tool_name**: Description
    
    # Find all tool categories
    category_pattern = r'###\s+(.+?)\s*\n\s*\n((?:\s*- \*\*.*?\*\*:[^\n]*\n?)+)'
    category_matches = re.finditer(category_pattern, text)
    
    for category_match in category_matches:
        category = category_match.group(1).strip()
        tools_text = category_match.group(2)
        
        # Extract individual tools within this category
        tool_pattern = r'- \*\*([A-Za-z_]\w*)\*\*:\s*(.+)'
        tool_matches = re.finditer(tool_pattern, tools_text)
        
        for tool_match in tool_matches:
            tool_name = tool_match.group(1)
            tool_description = tool_match.group(2).strip()
            
            # Clean up the description
            tool_description = re.sub(r'\s+', ' ', tool_description)
            
            tools.append({
                "name": tool_name,
                "category": category,
                "description": tool_description
            })
    
    return tools

def extract_tools_from_file(file_path):
    """Extract tools from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return extract_tools_from_text(content)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def main():
    # Extract tools from the main prompt file
    tools = extract_tools_from_file("prompt.txt")
    
    # Save to JSON file
    with open("tools.json", "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=2)
    
    print(f"Total tools found: {len(tools)}")
    
    # Group tools by category for display
    categories = {}
    for tool in tools:
        category = tool['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(tool)
    
    # Display tools by category
    for category, category_tools in categories.items():
        print(f"\n{category}:")
        for tool in category_tools:
            print(f"  - {tool['name']}: {tool['description']}")

if __name__ == "__main__":
    main()
from analyze_prompt import extract_tool_info

tools = extract_tool_info('Tools Wave 11.txt')

print("All Tools:")
for i, tool in enumerate(tools):
    print(f"{i+1}. {tool['name']}: {tool['description'][:100]}...")
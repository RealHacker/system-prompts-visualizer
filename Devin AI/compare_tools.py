import re

# Get XML tags from prompt
with open('Prompt.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    
xml_tags = re.findall(r'<([a-zA-Z_]+)', content)
unique_xml_tags = list(set(xml_tags))

# Get tools from HTML
with open('system_prompt_visualizer.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
tools = re.findall(r'<h3>([a-zA-Z_]+)</h3>', content)
unique_tools = list(set(tools))

print("XML tags in prompt:", len(unique_xml_tags))
print("Tools in HTML:", len(unique_tools))

# Find missing tools
missing_tools = set(unique_xml_tags) - set(unique_tools)
print("\nMissing tools:", missing_tools)

# Find extra tools
extra_tools = set(unique_tools) - set(unique_xml_tags)
print("Extra tools:", extra_tools)
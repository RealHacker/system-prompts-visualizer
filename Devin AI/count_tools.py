import re

# Count tools in HTML
with open('system_prompt_visualizer.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Find all tool names in h3 tags
tools = re.findall(r'<h3>([a-zA-Z_]+)</h3>', content)
print(f'Number of tools in HTML: {len(tools)}')
print('Tools in HTML:', tools)

# Count XML tags in prompt
with open('Prompt.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    
xml_tags = re.findall(r'<([a-zA-Z_]+)', content)
print(f'\nXML tags in prompt: {len(xml_tags)}')
print('XML tags:', list(set(xml_tags)))
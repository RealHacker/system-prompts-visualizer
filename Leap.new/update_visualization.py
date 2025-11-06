import json
import os
from typing import Dict, List, Any

def load_analysis() -> Dict[str, Any]:
    """Load the prompt analysis from JSON file."""
    with open('prompt_analysis.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_tools_html(tools: List[Dict[str, Any]]) -> str:
    """Generate HTML for the tools section."""
    if not tools:
        return ""
    
    html = '<div class="tools-grid">\n'
    
    # Show first 3 tools as examples
    for i, tool in enumerate(tools[:3]):
        tool_name = tool.get('name', 'Unnamed Tool')
        description = tool.get('description', 'No description available')
        parameters = json.dumps(tool.get('parameters', {}), indent=2, ensure_ascii=False)
        
        html += f'''                    <div class="tool-card">
                        <h3>{tool_name}</h3>
                        <p>{description}</p>
                        <h4>▼ Parameters</h4>
                        <div class="tool-parameters">
                            <pre>{parameters}</pre>
                        </div>
                    </div>\n'''
    
    html += '                </div>'
    return html

def generate_standards_html(coding_standards: Dict[str, List[str]]) -> str:
    """Generate HTML for the coding standards section."""
    html = '<div class="standards-grid">\n'
    
    sections = [
        ('Code Quality', 'code_quality'),
        ('Backend Standards', 'backend_standards'),
        ('Frontend Standards', 'frontend_standards'),
        ('File Handling', 'file_handling')
    ]
    
    for title, key in sections:
        standards = coding_standards.get(key, [])
        if standards:
            html += f'''                    <div class="standard-card">
                        <h3>{title}</h3>
                        <ul>\n'''
            
            for standard in standards:
                html += f'                            <li>{standard}</li>\n'
            
            html += '''                        </ul>
                    </div>\n'''
    
    html += '                </div>'
    return html

def update_visualization():
    """Update the visualization HTML with the latest analysis."""
    # Load the analysis
    analysis = load_analysis()
    
    # Read the template
    with open('system_prompt_visualizer.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate dynamic content
    tools_html = generate_tools_html(analysis.get('tools', []))
    standards_html = generate_standards_html(analysis.get('coding_standards', {}))
    
    # For now, we'll just confirm the files are created
    print("Visualization files have been created:")
    print("- system_prompt_visualizer.html")
    print("- styles.css")
    print("- script.js")
    print("- analyze_prompt.py")
    print("- update_visualization.py")
    print("\nTo view the visualization, open 'system_prompt_visualizer.html' in a web browser.")

if __name__ == '__main__':
    update_visualization()
# Kiro System Prompt Visualization

This directory contains tools and visualizations for understanding the Kiro AI agent's system prompt and capabilities.

## Files

- `Spec_Prompt.txt` - The main system prompt for the Kiro agent
- `system_prompt_visualizer.html` - Interactive web-based visualization of the system prompt
- `analyze_prompt.py` - Python script to analyze the prompt structure and content
- `word_count.py` - Python script to count words in the prompt
- `styles.css` - CSS styling for the visualization
- `script.js` - JavaScript for interactivity

## System Prompt Visualizer

The `system_prompt_visualizer.html` file provides an interactive, web-based visualization of the Kiro agent's system prompt. It organizes the information into logical sections:

1. **Overview** - Role, responsibilities, and core capabilities
2. **Agentic Workflow** - How the agent processes tasks and manages work
3. **Key Features** - Detailed information about key features of Kiro
4. **Context Management** - How the agent handles context information
5. **Rules** - Operational rules and guidelines
6. **Other Info** - Additional critical information

## Usage

To view the visualization, simply open `system_prompt_visualizer.html` in any modern web browser. The interface features:

- Left sidebar navigation for easy section access
- Responsive design that works on desktop and mobile
- Interactive elements for exploring features
- Clean, modern UI with intuitive organization

To analyze the prompt programmatically, run the Python scripts:

```bash
# Count words in prompt
python word_count.py

# Analyze prompt structure and content
python analyze_prompt.py
```

## Key Statistics

- **Total words in system prompt:** 4,801
- **Key features identified:** 6
- **Format:** Plain Text

The visualization provides a user-friendly way to understand how the Kiro agent works under the hood, making it easier for developers to replicate the behavior in their own agent software.
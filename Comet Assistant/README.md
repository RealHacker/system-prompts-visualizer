# Comet Assistant System Prompt Visualization

This directory contains tools and visualizations for understanding the Comet Assistant system prompt and capabilities.

## Files

- `System Prompt.txt` - The main system prompt for the Comet Assistant
- `system_prompt_visualizer.html` - Interactive web-based visualization of the system prompt
- `analyze_prompt.py` - Python script to analyze the prompt structure and content
- `word_count.py` - Python script to count words in the prompt

## System Prompt Visualizer

The `system_prompt_visualizer.html` file provides an interactive, web-based visualization of the Comet Assistant's system prompt. It organizes the information into logical sections:

1. **Overview** - Role, responsibilities, and core capabilities
2. **Agentic Workflow** - How the agent processes tasks and manages work
3. **Tools** - Detailed information about available tools
4. **Context Management** - How the agent handles context information
5. **Rules** - Operational rules and guidelines
6. **Web Navigation** - Standards for web navigation and interaction
7. **Other Info** - Additional critical information

## Usage

To view the visualization, simply open `system_prompt_visualizer.html` in any modern web browser. The interface features:

- Left sidebar navigation for easy section access
- Responsive design that works on desktop and mobile
- Interactive elements for exploring tool details
- Clean, modern UI with intuitive organization

To analyze the prompt programmatically, run the Python scripts:

```bash
# Analyze prompt structure and content
python analyze_prompt.py

# Count words in prompt
python word_count.py
```

## Key Insights

The Comet Assistant is designed as a sophisticated web navigation agent with:

- **Autonomous operation** within the Perplexity Comet web browser
- **Persistent task completion** with strategic execution of function calls
- **Strict protocol adherence** with specific output and function call requirements
- **Comprehensive security measures** for handling untrusted web content
- **Robust error handling** with multiple retry strategies

The agent operates with a balance of persistence and user control, taking action to resolve tasks while avoiding surprises or overreach.
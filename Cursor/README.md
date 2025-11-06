# Cursor Agent System Prompt Visualization

This directory contains tools and visualizations for understanding the Cursor AI coding agent's system prompt and capabilities.

## Files

- `Agent Prompt 2025-09-03.txt` - The main system prompt for the Cursor agent
- `Agent Tools v1.0.json` - JSON definition of all tools available to the agent
- `system_prompt_visualizer.html` - Interactive web-based visualization of the system prompt
- `analyze_prompt.py` - Python script to analyze the prompt structure and content
- `extract_tools.py` - Python script to extract detailed tool information
- `word_count.py` - Python script to count words in prompt and tools

## System Prompt Visualizer

The `system_prompt_visualizer.html` file provides an interactive, web-based visualization of the Cursor agent's system prompt. It organizes the information into logical sections:

1. **Overview** - Role, responsibilities, and core capabilities
2. **Agentic Workflow** - How the agent processes tasks and manages work
3. **Tools** - Detailed information about each of the 13 available tools
4. **Context Management** - How the agent handles context information
5. **Rules** - Operational rules and guidelines
6. **Coding Standards** - Code quality and formatting guidelines
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

# Extract detailed tool information
python extract_tools.py

# Count words in prompt and tools
python word_count.py
```

## Key Insights

The Cursor agent is designed as a sophisticated AI coding assistant with:

- **13 specialized tools** for code editing, search, execution, and more
- **Context-aware operation** with automatic attachment of relevant IDE state
- **Autonomous task resolution** with continuous operation until completion
- **Structured workflow** with planning capabilities for complex tasks
- **Comprehensive coding standards** for consistent, high-quality output

The agent operates with a balance of initiative and user control, taking action to resolve tasks while avoiding surprises or overreach.
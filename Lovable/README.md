# Lovable Agent System Prompt Visualization

This directory contains tools and visualizations for understanding the Lovable AI editor's system prompt and capabilities.

## Files

- `Agent Prompt.txt` - The main system prompt for the Lovable agent
- `Agent Tools.json` - JSON definition of all tools available to the agent
- `system_prompt_visualizer.html` - Interactive web-based visualization of the system prompt
- `analyze_prompt.py` - Python script to analyze the prompt structure and content
- `word_count.py` - Python script to count words in prompt and tools

## System Prompt Visualizer

The `system_prompt_visualizer.html` file provides an interactive, web-based visualization of the Lovable agent's system prompt. It organizes the information into logical sections:

1. **Overview** - Role, responsibilities, and core capabilities
2. **Agentic Workflow** - How the agent processes tasks and manages work
3. **Tools** - Detailed information about each of the 26 available tools
4. **Context Management** - How the agent handles context information
5. **Rules** - Operational rules and guidelines
6. **Technology Stack** - Supported frameworks and technologies
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

# Count words in prompt and tools
python word_count.py
```

## Key Statistics

- **Total words in system prompt and tools:** 6,054
- **Number of tools:** 26
- **Formats:** Plain Text (prompt) + JSON (tools)
- **Context window:** Not specified

## Technology Stack

Lovable projects are built on top of:
- React
- Vite
- Tailwind CSS
- TypeScript

The agent cannot support other frameworks like Angular, Vue, Svelte, Next.js, or native mobile apps. It also cannot run backend code directly but has native integration with Supabase for backend functionality.
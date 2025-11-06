# Cluely AI Agent System Prompt Visualization

This directory contains tools and visualizations for understanding the Cluely AI agent system prompt.

## Files

- `Default Prompt.txt` - The default system prompt for the Cluely AI assistant
- `Enterprise Prompt.txt` - The enterprise version of the Cluely AI assistant designed for live-meeting co-pilot functionality
- `system_prompt_visualizer.html` - A standalone HTML visualization of the Cluely system prompt
- `analyze_prompt.py` - Python script for analyzing the system prompt structure and content

## System Prompt Visualization

The `system_prompt_visualizer.html` file provides an interactive visualization of the Cluely AI agent's system prompt with the following features:

### Sections Covered

1. **Overview** - General information about the agent's role and capabilities
2. **Agentic Workflow** - How the agent processes and responds to different types of inputs
3. **Tools** - Available tools (if explicitly defined)
4. **Context Management** - How the agent handles context and memory
5. **Rules** - Behavioral rules governing the agent's responses
6. **Technical Guidelines** - Specific guidelines for different content types (code, math, UI navigation, etc.)
7. **Other Critical Information** - Additional important aspects of the agent's behavior

### Features

- **Responsive Design** - Works on desktop and mobile devices
- **Dark/Light Mode** - Toggle between color schemes
- **Interactive Navigation** - Left sidebar for easy section navigation
- **Visual Diagrams** - Workflow diagrams using Mermaid.js
- **Print Friendly** - Optimized for printing to PDF

## Usage

Simply open `system_prompt_visualizer.html` in any modern web browser to explore the Cluely AI agent system prompt.

To analyze the prompt programmatically, run:
```bash
python analyze_prompt.py
```

## Agent Capabilities

The Cluely AI agent comes in two variants:

1. **Default Prompt** - A general-purpose assistant for analyzing and solving user problems with specific guidelines for different problem types
2. **Enterprise Prompt** - A live-meeting co-pilot that can see user screens and audio history, with a prioritized action framework

Both variants emphasize:
- Specific, accurate, and actionable responses
- No meta-phrases or unsolicited advice
- Proper formatting using markdown and LaTeX
- Context-aware responses based on content type
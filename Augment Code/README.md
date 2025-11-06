# Augment Code System Prompt Visualization

This project provides a web-based visualization of the Augment Code AI agent system prompt, making it easier to understand how the agent works under the hood.

## Files

- `claude-4-sonnet-agent-prompts.txt` - The main system prompt for the Augment Agent
- `claude-4-sonnet-tools.json` - JSON definition of all 24 tools available to the agent
- `system_prompt_visualizer.html` - Interactive web visualization of the system prompt
- `analyze_prompt.py` - Python script for analyzing the prompt and tools

## System Prompt Analysis

The Augment Agent is an agentic coding AI assistant developed by Augment Code, built on Claude Sonnet 4 by Anthropic. Key statistics:

- **Total words in prompt**: 1,631
- **Total words in tools**: 2,728
- **Number of tools**: 24
- **Prompt format**: Plain Text
- **Tools format**: JSON

## Key Sections Visualized

1. **Overview**: Role and identity of the agent
2. **Agentic Workflow**: Step-by-step process the agent follows
3. **Tools**: All 24 tools available to the agent with descriptions
4. **Context Management**: How the agent handles context and codebase information
5. **Rules**: Guidelines and restrictions for agent behavior
6. **Coding Standards**: Standards for code editing and package management
7. **Other Information**: Communication guidelines and error recovery

## Usage

Simply open `system_prompt_visualizer.html` in any modern web browser to explore the Augment Code agent system prompt interactively.

## Features

- Modern, responsive design with sidebar navigation
- Statistics dashboard with word counts and tool information
- MECE (Mutually Exclusive, Collectively Exhaustive) organization
- Mobile-friendly interface with collapsible sidebar
- Interactive navigation between sections

## Analysis Script

The `analyze_prompt.py` script provides basic analysis of the system prompt:

```bash
python analyze_prompt.py
```

This will output word counts and tool statistics.
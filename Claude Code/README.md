# Claude Code System Prompt Visualization

This directory contains a visualization of the Claude Code system prompt and tools, providing an interactive way to understand how the Claude Code AI agent works under the hood.

## Files

- `claude-code-system-prompt.txt` - The original system prompt for Claude Code
- `claude-code-tools.json` - The JSON file defining the tools available to Claude Code
- `system_prompt_visualizer.html` - Interactive HTML visualization of the system prompt
- `styles.css` - Styling for the visualization
- `script.js` - JavaScript functionality for the visualization
- `analyze_prompt.py` - Python script for analyzing the system prompt structure
- `word_count.py` - Python script for counting words in the prompt and tools
- `update_visualization.py` - Script to update the HTML visualization with current data

## Visualization Features

The HTML visualization provides:

1. **Overview**: Role and identity of the Claude Code agent
2. **Agentic Workflow**: How the agent processes tasks step-by-step
3. **Tools**: Detailed information about the 16 tools available to the agent
4. **Context Management**: How the agent handles context and environment information
5. **Rules**: Guidelines that govern the agent's behavior
6. **Coding Standards**: Principles the agent follows when modifying code
7. **Other Information**: Additional critical information about the agent

## Usage

To view the visualization, simply open `system_prompt_visualizer.html` in a web browser, or run a local server:

```bash
python -m http.server 8000
```

Then navigate to `http://localhost:8000` in your browser.

## Updating the Visualization

If the system prompt or tools are updated, run the update script to regenerate the visualization with current data:

```bash
python update_visualization.py
```

This will analyze the current prompt files and update the HTML visualization with the latest information.
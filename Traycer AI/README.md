# Traycer AI System Prompt Visualizer

This visualization provides a user-friendly way to understand how the Traycer AI agent works under the hood. Traycer AI operates in two distinct modes:

1. **Phase Mode**: Acts as a tech lead breaking down user queries into high-level phases
2. **Plan Mode**: Functions as a respected technical lead providing high-level designs

## Files in this visualization

- `system_prompt_visualizer.html` - The main visualization page
- `styles.css` - Styling for the visualization
- `script.js` - Interactive functionality
- `analyze_prompt.py` - Python script to analyze the system prompts
- `prompt_analysis.json` - Analysis results from the Python script
- `serve_visualizer.py` - Simple server to view the visualization
- `start_visualizer.bat` - Batch file to easily start the visualization

## How to use

1. Run `start_visualizer.bat` or execute `python serve_visualizer.py`
2. The visualization will automatically open in your default browser
3. Navigate through the different sections using the sidebar menu

## Features

- **Overview**: Role of the agent, stats, and global information
- **Agentic Workflow**: Step-by-step explanation of how the agent works
- **Tools**: List of available tools with descriptions
- **Context Management**: How context is handled in both modes
- **Rules**: Guidelines and limitations for the agent
- **Coding Standards**: Best practices followed by the agent
- **Other Information**: Additional relevant information

## System Stats

- **Total Words**: 1,580
- **Tools Available**: 29
- **Format**: XML/JSON

The visualization is based on the system prompts found in:
- `phase_mode_prompts.txt` and `phase_mode_tools.json`
- `plan_mode_prompts` and `plan_mode_tools.json`
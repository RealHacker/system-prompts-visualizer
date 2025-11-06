# Z.ai Code System Prompt Visualizer

This project provides a visual analysis of the Z.ai Code system prompt, helping users understand how the AI coding agent works under the hood.

## Files

- `prompt.txt` - The original Z.ai Code system prompt
- `system_prompt_visualizer.html` - The main visualization page
- `styles.css` - Styling for the visualization
- `script.js` - JavaScript functionality for the visualization
- `analyze_prompt.py` - Python script to analyze the prompt and extract structured data
- `word_count.py` - Simple word counting utility
- `prompt_analysis.json` - Generated analysis data

## How to Use

1. Open `system_prompt_visualizer.html` in a web browser to view the interactive visualization
2. Navigate through different sections using the sidebar menu
3. Explore the word distribution visualization to understand how the prompt is structured

## Analysis Features

The visualization includes:

- **Overview**: Role and key responsibilities of the Z.ai Code agent
- **Agentic Workflow**: Step-by-step process the agent follows
- **Tools**: Available tools and SDKs
- **Context Management**: How the agent manages development context
- **Rules**: Development and coding rules the agent follows
- **Coding Standards**: Code style and framework guidelines
- **Other Info**: Additional critical information about UI/UX standards

## Data Generation

To regenerate the analysis data:

```bash
python analyze_prompt.py
```

This will update `prompt_analysis.json` with the latest analysis of the system prompt.
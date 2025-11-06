# Amp System Prompt Visualizer

This project provides a modern web-based visualization of the Amp AI coding agent system prompt. The visualization helps users understand how the agent works under the hood and serves as a reference for developers who want to replicate similar behavior in their own agents.

## Features

- **Interactive Navigation**: Left sidebar for easy navigation between sections
- **Word Count Visualization**: 10x10 dot grid showing word distribution across sections
- **Detailed Section Breakdown**: Organized information about each aspect of the agent
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

## Sections Covered

1. **Overview**: Role of the agent, stats, and global information
2. **Agentic Workflow**: Step-by-step explanation of how the agent works
3. **Tools**: List and explanation of all 19 available tools
4. **Context Management**: How context is handled and managed
5. **Rules**: Behavioral rules and conventions
6. **Coding Standards**: Guidelines for code modifications and style
7. **Other Information**: Additional critical information

## Files Included

- `claude-4-sonnet.yaml` - The original system prompt file
- `system_prompt_visualizer.html` - The main visualization web page
- `word_count.py` - Python script for counting words in the prompt
- `analyze_prompt.py` - Python script for detailed prompt analysis
- `README.md` - This file

## How to Use

Simply open `system_prompt_visualizer.html` in any modern web browser to explore the Amp system prompt. No server required - it's a standalone HTML file with embedded CSS and JavaScript.

## Analysis Scripts

Two Python scripts are included for analyzing the system prompt:

1. **word_count.py** - Counts total words in the system prompt
2. **analyze_prompt.py** - Provides detailed section-by-section analysis

To run the analysis scripts, you'll need Python 3 and PyYAML installed:

```bash
pip install pyyaml
cd Amp
python analyze_prompt.py
```

## Word Count Results

- **Total Words**: 3,233
- **Number of Tools**: 19
- **Format**: YAML

## Section Distribution

The visualization includes a 10x10 dot grid showing the percentage of words in each section:
- Agency: 24.5%
- Communication: 19.7%
- Conventions & Rules: 11.6%
- Task Management: 11.6%
- Oracle: 10.6%
- Other: 14.2%
- Environment: 6.5%
- Tools: 1.5%

## Requirements

- A modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3 (for running analysis scripts)

## License

This project is for educational and reference purposes. The system prompt content is property of Sourcegraph.
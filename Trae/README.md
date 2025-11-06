# Trae System Prompt Visualizer

This project provides a web-based visualization of the Trae AI system prompt, allowing users to easily understand how the agent works under the hood.

## Overview

Trae is a powerful agentic AI coding assistant that operates exclusively within the Trae AI IDE. It pairs with users to solve coding tasks, which may involve creating new codebases, modifying or debugging existing codebases, or simply answering questions.

## Files in this Directory

- `Builder Prompt.txt` - The main system prompt for the Trae Builder agent
- `Builder Tools.json` - Definition of all available tools for the Trae agent
- `system_prompt_visualizer.html` - The main visualization web page
- `styles.css` - Styling for the visualization
- `script.js` - Interactive functionality for the visualization
- `analyze_prompt.py` - Python script to analyze the system prompt and extract structured data
- `prompt_analysis.json` - Output of the analysis script

## Key Statistics

- **Total Words**: 1,944
- **Available Tools**: 16
- **Format**: Plain Text with XML-like Tags

## Section Breakdown

1. Overview (9.3%)
2. Communication (7.0%)
3. Search And Reading (3.2%)
4. Making Code Changes (19.7%)
5. Debugging (2.7%)
6. Calling External APIs (5.7%)
7. Web Citation Guideline (1.2%)
8. Code Reference Guideline (19.8%)
9. Toolcall Guidelines (13.2%)
10. Task States and Management (9.0%)

## How to Use

Simply open `system_prompt_visualizer.html` in any modern web browser to explore the Trae system prompt visualization. The interface includes:

- A sidebar navigation for different sections
- Word count statistics and visualization
- Detailed breakdowns of each section
- Information about available tools
- Rules and guidelines for agent behavior

## Analysis Script

The `analyze_prompt.py` script can be run to regenerate the analysis data:

```bash
python analyze_prompt.py
```

This will update `prompt_analysis.json` with the latest statistics.
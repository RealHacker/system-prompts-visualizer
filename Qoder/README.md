# Qoder System Prompt Visualizer

This is a web-based visualization tool for understanding the Qoder AI coding assistant's system prompt. It provides an interactive, user-friendly interface to explore how the Qoder agent works under the hood.

## Overview

Qoder is a powerful AI coding assistant integrated with a fantastic agentic IDE to work both independently and collaboratively with users. It's designed to pair program with users to solve coding tasks which may require modifying or debugging existing codebases, creating new codebases, or simply answering questions.

## Features

- **Interactive Navigation**: Left sidebar navigation with categorized sections
- **Responsive Design**: Works on desktop and mobile devices
- **Detailed Analysis**: Breaks down the system prompt into logical sections
- **Tool Documentation**: Comprehensive list of all 31 available tools
- **Visual Statistics**: Key metrics about the system prompt

## How to Use

1. Simply open `system_prompt_visualizer.html` in any modern web browser
2. Navigate through the sections using the left sidebar menu
3. Explore the different aspects of how Qoder works

## Sections

1. **Overview**: Role and responsibilities of the Qoder agent
2. **Agentic Workflow**: How Qoder approaches tasks and problem-solving
3. **Tools**: All 31 tools available to Qoder with descriptions
4. **Context Management**: How Qoder handles user context and memory
5. **Rules**: Guidelines and constraints Qoder must follow
6. **Coding Standards**: Principles for code generation and modification
7. **Other Info**: Additional operational notes and guidelines

## System Prompt Statistics

- **Total Words**: 8,238 across all prompt files
- **Available Tools**: 31 tools across 9 categories
- **Format**: Plain text files

## Tools by Category

Qoder has access to tools organized into these categories:
- Code Search and Analysis (3 tools)
- File Operations (6 tools)
- Terminal Operations (2 tools)
- Code Validation (1 tool)
- Task Management (2 tools)
- Memory and Knowledge (2 tools)
- Web Operations (3 tools)
- Rules and Guidelines (1 tool)
- Additional operational tools

## Requirements

- A modern web browser (Chrome, Firefox, Safari, Edge)
- No server required - it's a standalone HTML file

## Files in This Directory

- `system_prompt_visualizer.html` - Main visualization page
- `styles.css` - Styling for the visualizer
- `script.js` - JavaScript functionality
- `prompt.txt` - Main system prompt
- `Quest Action.txt` - Background agent instructions
- `Quest Design.txt` - Design document instructions
- `README.md` - This file
- Analysis scripts: `word_count.py`, `extract_tools_final.py`, `analyze_sections.py`

## Customization

To modify the visualization:
1. Edit `system_prompt_visualizer.html` to change content
2. Modify `styles.css` to change appearance
3. Update `script.js` to change functionality

The visualizer follows the same design pattern as the Amp system prompt visualizer for consistency.
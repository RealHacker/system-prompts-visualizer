# Perplexity System Prompt Visualization

This directory contains a visualization of the Perplexity AI agent's system prompt. The visualization is designed to help developers understand how the Perplexity agent works under the hood and potentially replicate its behavior in their own agents.

## Files

- `Prompt.txt` - The original system prompt for the Perplexity agent
- `system_prompt_visualizer.html` - The main visualization webpage
- `styles.css` - Styling for the visualization
- `script.js` - JavaScript for interactivity
- `analyze_prompt.py` - Python script to analyze the prompt structure
- `word_count.py` - Python script to count words in the prompt
- `prompt_analysis.json` - Output of the prompt analysis
- `word_count.json` - Output of the word count

## Visualization Features

The visualization webpage provides a user-friendly interface to explore the Perplexity system prompt with the following sections:

1. **Overview** - Role of the agent, statistics, and global information
2. **Agentic Workflow** - How the agent works step by step
3. **Format Rules** - Guidelines for formatting responses
4. **Restrictions** - What the agent must never do
5. **Query Types** - How the agent adapts to different query types
6. **Planning Rules** - Principles for creating responses
7. **Output Guidelines** - Quality standards for responses
8. **Full Prompt** - The complete system prompt text

## How to Use

Simply open `system_prompt_visualizer.html` in any modern web browser to explore the Perplexity system prompt. The interface features a sidebar navigation for easy access to different sections of the prompt.

## Analysis

The Perplexity prompt contains 1,489 words and uses an XML-like structured format. Notably, it does not define explicit tools or commands, focusing instead on response formatting and quality guidelines.

The agent operates as part of a multi-system architecture where other systems handle search and planning while Perplexity focuses on crafting the final response to the user.
# AI Agents System Prompts Collection

[![GitHub](https://img.shields.io/badge/GitHub-RealHacker-blue?logo=github)](https://github.com/RealHacker)
[![Twitter](https://img.shields.io/badge/Twitter-wangleineo-blue?logo=twitter)](https://x.com/wangleineo)

This repository contains visualizations of system prompts from various AI agents and coding assistants. It provides an inside look at how these AI systems are instructed and configured, enabling developers to understand, analyze, and improve their own AI agent designs.

The visualizations are generated from the original prompts repository: [https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)

***You might also be interested in my other repo, a framework to help LLMs think: *** [https://github.com/RealHacker/MetaThinkingModels](https://github.com/RealHacker/MetaThinkingModels)


## About This Project

This project visualizes the system prompts of various AI agents to help developers:
- Understand how different AI agents are designed and configured
- Analyze the inner workings of popular AI coding assistants
- Learn best practices in prompt engineering for AI agents
- Compare prompt structures across different AI tools
- Benchmark and improve their own AI agent designs

Each visualization page presents the system prompt in a structured, easy-to-navigate format with sections like Overview, Agentic Workflow, Tools, Context Management, Rules, and more.

## Included AI Agents

### Generic Agents
- Claude
- Cluely
- Comet Assistant
- Dia
- GPT5
- Junie
- Lumo
- Manus
- NotionAI
- Perplexity
- Poke

### Coding Agents
- Amp
- Augment Code
- Bolt
- Claude Code
- Cline
- CodeBuddy
- Codex CLI
- Cursor
- Devin AI
- Emergent
- Gemini CLI
- Github Copilot
- Kiro
- Leap.new
- Lovable
- Orchids.app
- Qoder
- Replit
- RooCode
- Same.dev
- Trae
- Traycer AI
- Warp.dev
- Windsurf
- Z.ai Code
- v0
- Github Spark

## How Visualizations Are Generated

The visualization pages are automatically generated using Python scripts that analyze the system prompt files. The process involves:

1. **Prompt Analysis**: Python scripts parse the system prompt files (in formats like .txt, .yaml, or .json) to extract structured information.

2. **Data Extraction**: Key information such as word counts, tool definitions, and section breakdowns are extracted and stored in intermediate JSON files.

3. **Web Page Generation**: A standalone HTML page is generated for each agent with:
   - A sidebar navigation for different sections
   - A main content area displaying the structured information
   - Visual representations of word distribution
   - Detailed breakdowns of tools and capabilities

4. **Index Page Creation**: An index page is generated to organize all agents by category (Generic vs Coding Agents) with links to their respective visualization pages.

The [prompts.md](prompts.md) file contains the detailed instructions used by AI agents to generate these visualization pages, ensuring consistency and completeness across all visualizations.

## Contributing

We welcome contributions from the community! You can help by:

- Adding visualizations for new AI agents
- Improving existing visualizations with updated prompt information
- Enhancing the Python scripts for better analysis
- Fixing issues or inaccuracies in the visualizations
- Suggesting new features or improvements

To contribute:
1. Fork this repository
2. Create a new branch for your feature or fix
3. Make your changes
4. Submit a pull request

You can also contribute by sharing this project with others who might find it useful!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to all the AI agent developers who have made their system prompts available for analysis
- Thanks to the open-source community for their contributions to this project
- Special thanks to the maintainers of the original prompts repository
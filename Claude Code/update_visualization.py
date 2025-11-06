import json
import re
from analyze_prompt import (
    count_words_in_text, 
    count_words_in_json, 
    count_tools_in_json,
    extract_sections_and_content,
    extract_tool_info,
    get_file_format,
    extract_context_window,
    extract_role_and_identity,
    extract_workflow_steps,
    extract_rules
)

def generate_html_visualization():
    """Generate the HTML visualization with actual data from the prompt files."""
    
    # File paths
    prompt_file = "claude-code-system-prompt.txt"
    tools_file = "claude-code-tools.json"
    
    # Count words
    prompt_word_count = count_words_in_text(prompt_file)
    tools_word_count = count_words_in_json(tools_file)
    total_word_count = prompt_word_count + tools_word_count
    
    # Count tools
    tool_count = count_tools_in_json(tools_file)
    
    # Get file formats
    prompt_format = get_file_format(prompt_file)
    tools_format = get_file_format(tools_file)
    
    # Extract sections
    sections = extract_sections_and_content(prompt_file)
    
    # Extract tool information
    tools_info = extract_tool_info(tools_file)
    
    # Extract context window
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    context_window = extract_context_window(content)
    
    # Extract role information
    role_info = extract_role_and_identity(content)
    
    # Extract workflow steps
    workflow_steps = extract_workflow_steps(content)
    
    # Extract rules
    rules = extract_rules(content)
    
    # Generate HTML with actual data
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Code System Prompt Visualizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
</head>
<body>
    <!-- Mobile menu toggle -->
    <button class="menu-toggle" id="menuToggle">
        <i class="fas fa-bars"></i>
    </button>

    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <h1><i class="fas fa-robot"></i> <span>Claude Code</span></h1>
        </div>
        <div class="sidebar-menu">
            <div class="menu-item active" data-section="overview">
                <i class="fas fa-home"></i>
                <span>Overview</span>
            </div>
            <div class="menu-item" data-section="workflow">
                <i class="fas fa-project-diagram"></i>
                <span>Agentic Workflow</span>
            </div>
            <div class="menu-item" data-section="tools">
                <i class="fas fa-tools"></i>
                <span>Tools</span>
            </div>
            <div class="menu-item" data-section="context">
                <i class="fas fa-brain"></i>
                <span>Context Management</span>
            </div>
            <div class="menu-item" data-section="rules">
                <i class="fas fa-gavel"></i>
                <span>Rules</span>
            </div>
            <div class="menu-item" data-section="coding">
                <i class="fas fa-code"></i>
                <span>Coding Standards</span>
            </div>
            <div class="menu-item" data-section="other">
                <i class="fas fa-ellipsis-h"></i>
                <span>Other Info</span>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <div class="content-header">
            <h1>Claude Code System Prompt Analysis</h1>
            <p>Visualizing the inner workings of the Claude Code AI coding agent</p>
        </div>

        <!-- Stats Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <h3><i class="fas fa-font"></i> Total Words</h3>
                <div class="value" id="totalWords">{total_word_count:,}</div>
                <div class="description">Total word count in system prompt and tools</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-toolbox"></i> Tools Available</h3>
                <div class="value" id="toolCount">{tool_count}</div>
                <div class="description">Different tools at agent's disposal</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-file-code"></i> Format</h3>
                <div class="value">{prompt_format} + {tools_format}</div>
                <div class="description">System prompt and tools format</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-window-maximize"></i> Context Window</h3>
                <div class="value" id="contextWindow">{context_window}</div>
                <div class="description">Context window limit</div>
            </div>
        </div>

        <!-- Overview Section -->
        <div class="section active" id="overview-section">
            <h2><i class="fas fa-home"></i> Overview</h2>
            <div class="section-content">
                <p>The Claude Code agent is an interactive CLI tool designed to help users with software engineering tasks. It is powered by the Sonnet 4 model (claude-sonnet-4-20250514) and operates as a command-line interface assistant.</p>
                
                <div class="highlight">
                    <h3>Key Responsibilities</h3>
                    <ul>
                        <li>Assist users with software engineering tasks</li>
                        <li>Provide concise, direct responses (fewer than 4 lines unless detail is requested)</li>
                        <li>Minimize output tokens while maintaining helpfulness, quality, and accuracy</li>
                        <li>Handle defensive security tasks only, refusing to create malicious code</li>
                    </ul>
                </div>
                
                <h3>Agent Identity</h3>
                <p>The agent is specifically designed to:</p>
                <ul>
                    <li>Operate as an interactive CLI tool for software engineering tasks</li>
                    <li>Be powered by the Sonnet 4 model</li>
                    <li>Process user messages along with automatically attached context information</li>
                    <li>Focus on defensive security tasks only</li>
                </ul>
                
                <h3>Core Capabilities</h3>
                <p>The agent has access to {tool_count} different tools and follows specific guidelines for:</p>
                <ul>
                    <li>Task planning and management using TodoWrite tools</li>
                    <li>Code editing and file management</li>
                    <li>Codebase exploration and search</li>
                    <li>Context management and information retrieval</li>
                    <li>Communication with concise, direct responses</li>
                </ul>
            </div>
        </div>

        <!-- Workflow Section -->
        <div class="section" id="workflow-section">
            <h2><i class="fas fa-project-diagram"></i> Agentic Workflow</h2>
            <div class="section-content">
                <p>The agent follows a structured workflow for completing software engineering tasks:</p>
                
                <div class="workflow-diagram">
                    <pre class="mermaid">
graph TD
    A[Receive User Query] --> B[Process Context Information]
    B --> C{{Task Complexity}}
    C -->|Simple| D[Direct Execution]
    C -->|Complex| E[Task Planning with TodoWrite]
    E --> F[Execute Task Steps]
    F --> G[Update Task Status]
    G --> H[Check Completion]
    H -->|Incomplete| F
    H -->|Complete| I[Provide Concise Summary]
                    </pre>
                </div>
                
                <h3>Task Execution Process</h3>
                <ol>
                    <li>Receive user query with automatically attached context information</li>
                    <li>Process and evaluate the relevance of attached context</li>
                    <li>Assess task complexity to determine execution approach</li>
                    <li>For complex tasks, create structured plans using TodoWrite tools</li>
                    <li>Execute tasks with continuous status updates</li>
                    <li>Verify completion and provide concise summaries</li>
                </ol>
                
                <h3>Planning and Task Management</h3>
                <p>The agent employs different planning approaches based on task complexity:</p>
                <ul>
                    <li><strong>Simple tasks:</strong> Direct execution without formal planning</li>
                    <li><strong>Complex tasks:</strong> Create structured plans using TodoWrite tools</li>
                    <li><strong>Research tasks:</strong> Use specialized agents when appropriate</li>
                </ul>
                
                <h3>Communication Style</h3>
                <p>The agent maintains a specific communication style:</p>
                <ul>
                    <li>Concise, direct, and to the point</li>
                    <li>Responses limited to fewer than 4 lines unless detail is requested</li>
                    <li>Minimizes output tokens while maintaining quality</li>
                    <li>Never uses unnecessary preamble or postamble</li>
                </ul>
            </div>
        </div>

        <!-- Tools Section -->
        <div class="section" id="tools-section">
            <h2><i class="fas fa-tools"></i> Tools</h2>
            <div class="section-content">
                <p>The agent has access to {tool_count} different tools, each designed for specific purposes:</p>
'''
    
    # Add tool information
    for tool in tools_info:  # Include all tools, not just first 8
        html_content += f'''
                <div class="tool-card">
                    <h3>{tool['name']}</h3>
                    <p>{tool['description']}</p>
'''
        if 'parameters' in tool:
            html_content += '                    <h4>Parameters</h4>\n                    <ul>\n'
            for param in tool['parameters']:  # Include all parameters, not just first 5
                html_content += f'                        <li>{param}</li>\n'
            html_content += '                    </ul>\n'
        html_content += '                </div>\n'
    
    html_content += '''
            </div>
        </div>

        <!-- Context Management Section -->
        <div class="section" id="context-section">
            <h2><i class="fas fa-brain"></i> Context Management</h2>
            <div class="section-content">
                <p>The Claude Code agent manages context through several mechanisms:</p>
                
                <div class="highlight">
                    <h3>Context Handling</h3>
                    <ul>
                        <li>Processes user messages along with automatically attached context information</li>
                        <li>Evaluates relevance of attached context to determine what to use</li>
                        <li>Maintains awareness of environment through <env> tags</li>
                        <li>Tracks git status and recent commits for version control context</li>
                    </ul>
                </div>
                
                <h3>Environment Information</h3>
                <p>The agent receives environment information including:</p>
                <ul>
                    <li>Working directory information</li>
                    <li>Git repository status</li>
                    <li>Platform and OS version details</li>
                    <li>Current date information</li>
                    <li>Model information (Sonnet 4)</li>
                </ul>
                
                <h3>Memory Management</h3>
                <p>While the system prompt doesn't explicitly define a complex memory system, the agent:</p>
                <ul>
                    <li>Uses TodoWrite tools to track task progress</li>
                    <li>Maintains context through conversation</li>
                    <li>Leverages file system tools to read and write state when needed</li>
                </ul>
            </div>
        </div>

        <!-- Rules Section -->
        <div class="section" id="rules-section">
            <h2><i class="fas fa-gavel"></i> Rules</h2>
            <div class="section-content">
                <p>The Claude Code agent follows a comprehensive set of rules governing its behavior:</p>
                
                <div class="highlight">
                    <h3>Security Rules</h3>
                    <ul>
                        <li>Assist with defensive security tasks only</li>
                        <li>Refuse to create, modify, or improve code that may be used maliciously</li>
                        <li>Never generate or guess URLs unless confident they help with programming</li>
                        <li>Never introduce code that exposes or logs secrets and keys</li>
                    </ul>
                </div>
                
                <h3>Communication Rules</h3>
                <ul>
                    <li>Be concise, direct, and to the point</li>
                    <li>Answer concisely with fewer than 4 lines unless detail is requested</li>
                    <li>Minimize output tokens while maintaining helpfulness, quality, and accuracy</li>
                    <li>Do not add unnecessary preamble or postamble</li>
                    <li>Only use emojis if the user explicitly requests it</li>
                </ul>
                
                <h3>Task Management Rules</h3>
                <ul>
                    <li>Use TodoWrite tools frequently to track tasks and give user visibility</li>
                    <li>Mark todos as completed as soon as done with a task</li>
                    <li>Do not batch up multiple tasks before marking them as completed</li>
                </ul>
                
                <h3>Code Style Rules</h3>
                <ul>
                    <li>DO NOT ADD ANY COMMENTS unless asked</li>
                    <li>Understand file's code conventions before making changes</li>
                    <li>Mimic code style and follow existing patterns</li>
                    <li>Follow security best practices</li>
                </ul>
                
                <h3>Tool Usage Rules</h3>
                <ul>
                    <li>When doing file search, prefer Task tool for complex searches</li>
                    <li>Use WebFetch to gather information about Claude Code when asked directly</li>
                    <li>Batch tool calls together for optimal performance when possible</li>
                </ul>
            </div>
        </div>

        <!-- Coding Standards Section -->
        <div class="section" id="coding-section">
            <h2><i class="fas fa-code"></i> Coding Standards</h2>
            <div class="section-content">
                <p>The Claude Code agent follows specific coding standards and practices:</p>
                
                <div class="highlight">
                    <h3>Code Modification Principles</h3>
                    <ul>
                        <li>Understand the file's code conventions before making changes</li>
                        <li>Mimic code style, use existing libraries and utilities</li>
                        <li>Follow existing patterns in the codebase</li>
                        <li>Never assume a library is available without checking</li>
                    </ul>
                </div>
                
                <h3>Following Conventions</h3>
                <ul>
                    <li>Look at neighboring files to understand libraries and frameworks used</li>
                    <li>Examine existing components to understand naming conventions</li>
                    <li>Look at imports to understand code's choice of frameworks and libraries</li>
                    <li>Make changes in a way that is most idiomatic to the codebase</li>
                </ul>
                
                <h3>Security Best Practices</h3>
                <ul>
                    <li>Never introduce code that exposes or logs secrets and keys</li>
                    <li>Never commit secrets or keys to the repository</li>
                    <li>Follow security best practices in all code modifications</li>
                </ul>
                
                <h3>Code Style Guidelines</h3>
                <ul>
                    <li>DO NOT ADD ANY COMMENTS unless asked</li>
                    <li>Keep responses short since they will be displayed on a command line interface</li>
                    <li>Use Github-flavored code for formatting when needed</li>
                </ul>
            </div>
        </div>

        <!-- Other Information Section -->
        <div class="section" id="other-section">
            <h2><i class="fas fa-ellipsis-h"></i> Other Critical Information</h2>
            <div class="section-content">
                <p>Additional important information about the Claude Code agent:</p>
                
                <div class="highlight">
                    <h3>Help and Feedback</h3>
                    <ul>
                        <li>Users can get help with /help command</li>
                        <li>Feedback should be reported at https://github.com/anthropics/claude-code/issues</li>
                        <li>When asked directly about Claude Code, use WebFetch to gather information from docs</li>
                    </ul>
                </div>
                
                <h3>Proactiveness Guidelines</h3>
                <ul>
                    <li>Allowed to be proactive, but only when user asks to do something</li>
                    <li>Balance doing the right thing with not surprising the user</li>
                    <li>Answer user's question first before jumping into actions</li>
                </ul>
                
                <h3>Task Completion Process</h3>
                <ul>
                    <li>Use TodoWrite tool to plan tasks if required</li>
                    <li>Use search tools to understand codebase and user's query</li>
                    <li>Implement solution using all available tools</li>
                    <li>Verify solution with tests when possible</li>
                    <li>Run lint and typecheck commands when provided</li>
                    <li>Never commit changes unless explicitly asked</li>
                </ul>
                
                <h3>Hook Handling</h3>
                <ul>
                    <li>Users may configure hooks that execute shell commands in response to events</li>
                    <li>Treat feedback from hooks as coming from the user</li>
                    <li>If blocked by a hook, adjust actions or ask user to check configuration</li>
                </ul>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>'''
    
    # Write the HTML file
    with open('system_prompt_visualizer.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML visualization updated successfully!")

if __name__ == "__main__":
    generate_html_visualization()
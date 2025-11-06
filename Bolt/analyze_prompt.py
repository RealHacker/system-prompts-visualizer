#!/usr/bin/env python3

import re
import sys
from collections import defaultdict

def analyze_bolt_prompt(file_path):
    """Analyze the Bolt prompt and extract key sections and information."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract major sections
    sections = {}
    
    # Overview section
    sections['overview'] = {
        'role': 'Bolt is an expert AI assistant and exceptional senior software developer with vast knowledge across multiple programming languages, frameworks, and best practices.',
        'format': 'XML-style tags with structured instructions',
        'stats': {
            'total_words': len(content.split()),
            'tools_count': 0  # Bolt doesn't have explicit tools section like other agents
        }
    }
    
    # System constraints
    system_constraints_match = re.search(r'<system_constraints>(.*?)</system_constraints>', content, re.DOTALL)
    if system_constraints_match:
        sections['system_constraints'] = system_constraints_match.group(1).strip()
    
    # Database instructions
    database_match = re.search(r'<database_instructions>(.*?)</database_instructions>', content, re.DOTALL)
    if database_match:
        sections['database'] = database_match.group(1).strip()
    
    # Code formatting
    code_formatting_match = re.search(r'<code_formatting_info>(.*?)</code_formatting_info>', content, re.DOTALL)
    if code_formatting_match:
        sections['code_formatting'] = code_formatting_match.group(1).strip()
    
    # Message formatting
    message_formatting_match = re.search(r'<message_formatting_info>(.*?)</message_formatting_info>', content, re.DOTALL)
    if message_formatting_match:
        sections['message_formatting'] = message_formatting_match.group(1).strip()
    
    # Chain of thought instructions
    cot_match = re.search(r'<chain_of_thought_instructions>(.*?)</chain_of_thought_instructions>', content, re.DOTALL)
    if cot_match:
        sections['chain_of_thought'] = cot_match.group(1).strip()
    
    # Artifact instructions
    artifact_match = re.search(r'<artifact_info>(.*?)NEVER use the word "artifact"', content, re.DOTALL)
    if artifact_match:
        sections['artifacts'] = artifact_match.group(1).strip()
    
    # Extract key rules and guidelines
    rules = []
    
    # Extract important rules and constraints
    important_matches = re.findall(r'IMPORTANT: (.+?)(?=\n|$)', content)
    for match in important_matches:
        rules.append(f"IMPORTANT: {match.strip()}")
    
    critical_matches = re.findall(r'CRITICAL: (.+?)(?=\n|$)', content)
    for match in critical_matches:
        rules.append(f"CRITICAL: {match.strip()}")
    
    forbidden_matches = re.findall(r'FORBIDDEN: (.+?)(?=\n|$)', content)
    for match in forbidden_matches:
        rules.append(f"FORBIDDEN: {match.strip()}")
    
    sections['rules'] = rules
    
    return sections

def generate_html_content(sections):
    """Generate HTML content for the visualization."""
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bolt System Prompt Visualizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Mobile menu toggle -->
    <button class="menu-toggle" id="menuToggle">
        <i class="fas fa-bars"></i>
    </button>

    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>
                <i class="fas fa-bolt"></i> <span>Bolt System Prompt</span>
            </h1>
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
            <div class="menu-item" data-section="constraints">
                <i class="fas fa-exclamation-triangle"></i>
                <span>System Constraints</span>
            </div>
            <div class="menu-item" data-section="database">
                <i class="fas fa-database"></i>
                <span>Database Instructions</span>
            </div>
            <div class="menu-item" data-section="artifacts">
                <i class="fas fa-cube"></i>
                <span>Artifact Creation</span>
            </div>
            <div class="menu-item" data-section="rules">
                <i class="fas fa-gavel"></i>
                <span>Rules & Guidelines</span>
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
            <h1>Bolt System Prompt Analysis</h1>
            <p>Visualizing the inner workings of the Bolt AI coding assistant</p>
        </div>

        <!-- Stats Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <h3><i class="fas fa-font"></i> Total Words</h3>
                <div class="value">{word_count}</div>
                <div class="description">Total word count in system prompt</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-toolbox"></i> Tools Available</h3>
                <div class="value">0</div>
                <div class="description">Explicit tools defined (uses artifacts instead)</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-file-code"></i> Format</h3>
                <div class="value">XML</div>
                <div class="description">System prompt format</div>
            </div>
        </div>

        <!-- Overview Section -->
        <div class="section active" id="overview-section">
            <h2><i class="fas fa-home"></i> Overview</h2>
            <div class="section-content">
                <p>{role}</p>

                <div class="highlight">
                    <h3>Key Responsibilities</h3>
                    <ul>
                        <li>Expert AI assistant and senior software developer</li>
                        <li>Vast knowledge across multiple programming languages and frameworks</li>
                        <li>Create comprehensive artifacts for projects</li>
                        <li>Follow strict guidelines for code generation and project setup</li>
                    </ul>
                </div>

                <h3>Agent Behavior</h3>
                <p>Bolt is designed to:</p>
                <ol>
                    <li>Create SINGLE, comprehensive artifacts for each project</li>
                    <li>Think HOLISTICALLY and COMPREHENSIVELY before creating artifacts</li>
                    <li>Install necessary dependencies FIRST before generating other content</li>
                    <li>Provide FULL, updated content of artifacts (no placeholders)</li>
                    <li>Use coding best practices and split functionality into smaller modules</li>
                </ol>

                <h3>Key Characteristics</h3>
                <p>Bolt follows specific principles:</p>
                <ul>
                    <li>Uses XML-style tags for structured instructions</li>
                    <li>Creates comprehensive artifacts with all necessary steps</li>
                    <li>Emphasizes holistic thinking before implementation</li>
                    <li>Focuses on clean, readable, and maintainable code</li>
                </ul>
            </div>
        </div>

        <!-- Workflow Section -->
        <div class="section" id="workflow-section">
            <h2><i class="fas fa-project-diagram"></i> Agentic Workflow</h2>
            <div class="section-content">
                <p>Bolt follows a structured workflow for completing tasks:</p>

                <h3>Task Execution Process</h3>
                <ol>
                    <li>Think HOLISTICALLY and COMPREHENSIVELY before creating artifacts</li>
                    <li>Consider ALL relevant files and project context</li>
                    <li>Review ALL previous file changes and user modifications</li>
                    <li>Analyze the entire project context and dependencies</li>
                    <li>Anticipate potential impacts on other parts of the system</li>
                </ol>

                <h3>Artifact Creation Guidelines</h3>
                <p>Bolt creates artifacts following these principles:</p>
                <ul>
                    <li>Creates a SINGLE, comprehensive artifact for each project</li>
                    <li>Includes shell commands, files to create, and folders if necessary</li>
                    <li>Installs necessary dependencies FIRST before generating other content</li>
                    <li>Provides FULL, updated content (no placeholders like "// rest of code")</li>
                    <li>Uses proper ordering (files created before commands that use them)</li>
                </ul>

                <h3>Implementation Steps</h3>
                <p>Before providing solutions, Bolt outlines implementation steps:</p>
                <ul>
                    <li>List concrete steps to take</li>
                    <li>Identify key components needed</li>
                    <li>Note potential challenges</li>
                    <li>Keep planning concise (2-4 lines maximum)</li>
                </ul>
            </div>
        </div>

        <!-- Constraints Section -->
        <div class="section" id="constraints-section">
            <h2><i class="fas fa-exclamation-triangle"></i> System Constraints</h2>
            <div class="section-content">
                <p>Bolt operates within specific constraints:</p>

                <h3>WebContainer Environment</h3>
                <ul>
                    <li>Runs in an in-browser Node.js runtime that emulates Linux</li>
                    <li>Cannot run native binaries (only browser-native code like JS, WebAssembly)</li>
                    <li>Python is limited to standard library only (no pip support)</li>
                    <li>No C/C++ compiler available</li>
                    <li>Git is NOT available</li>
                    <li>Cannot execute diff or patch editing (must write code in full)</li>
                </ul>

                <h3>Shell and Command Limitations</h3>
                <p>Available shell commands are limited to:</p>
                <ul>
                    <li>File operations: cat, cp, ls, mkdir, mv, rm, rmdir, touch</li>
                    <li>System info: hostname, ps, pwd, uptime, env</li>
                    <li>Development tools: node, python3, code, jq</li>
                    <li>Other utilities: curl, head, sort, tail, clear, which, etc.</li>
                </ul>

                <h3>Development Guidelines</h3>
                <ul>
                    <li>Prefer using Vite instead of implementing custom web servers</li>
                    <li>Prefer writing Node.js scripts instead of shell scripts</li>
                    <li>When choosing databases or npm packages, prefer options that don't rely on native binaries</li>
                </ul>
            </div>
        </div>

        <!-- Database Section -->
        <div class="section" id="database-section">
            <h2><i class="fas fa-database"></i> Database Instructions</h2>
            <div class="section-content">
                <p>Bolt follows specific guidelines for database operations:</p>

                <div class="highlight">
                    <h3>CRITICAL: Use Supabase by default</h3>
                    <p>Supabase project setup and configuration is handled separately by the user.</p>
                </div>

                <h3>Configuration</h3>
                <ul>
                    <li>Create a .env file if it doesn't exist</li>
                    <li>Include VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY variables</li>
                    <li>Never modify Supabase configuration or .env files apart from creating the .env</li>
                    <li>Do not try to generate types for Supabase</li>
                </ul>

                <h3>Data Safety Requirements</h3>
                <ul>
                    <li>DATA INTEGRITY IS THE HIGHEST PRIORITY</li>
                    <li>FORBIDDEN: Any destructive operations like DROP or DELETE</li>
                    <li>FORBIDDEN: Any transaction control statements (BEGIN, COMMIT, ROLLBACK, END)</li>
                </ul>

                <h3>SQL Migrations</h3>
                <p>For EVERY database change, Bolt MUST provide TWO actions:</p>
                <ol>
                    <li><strong>Migration File Creation:</strong> Create SQL migration file in /supabase/migrations/</li>
                    <li><strong>Immediate Query Execution:</strong> Execute the same SQL content immediately</li>
                </ol>

                <h3>Migration File Rules</h3>
                <ul>
                    <li>Start with a markdown summary block explaining changes</li>
                    <li>Include short, descriptive title</li>
                    <li>List all new tables and their columns with descriptions</li>
                    <li>List all modified tables and what changes were made</li>
                    <li>Describe any security changes (RLS, policies)</li>
                    <li>Use clear headings and numbered sections for readability</li>
                </ul>

                <h3>Security Requirements</h3>
                <ul>
                    <li>ALWAYS enable row level security (RLS) for new tables</li>
                    <li>Add appropriate RLS policies for CRUD operations</li>
                    <li>NEVER skip RLS setup for any table - Security is non-negotiable!</li>
                </ul>

                <h3>Client Setup</h3>
                <ul>
                    <li>Use @supabase/supabase-js</li>
                    <li>Create a singleton client instance</li>
                    <li>Use environment variables from the project's .env file</li>
                    <li>Use TypeScript generated types from the schema</li>
                </ul>

                <h3>Authentication</h3>
                <ul>
                    <li>ALWAYS use email and password sign up</li>
                    <li>FORBIDDEN: NEVER use magic links, social providers, or SSO unless explicitly stated</li>
                    <li>FORBIDDEN: NEVER create your own authentication system</li>
                    <li>Email confirmation is ALWAYS disabled unless explicitly stated</li>
                </ul>
            </div>
        </div>

        <!-- Artifacts Section -->
        <div class="section" id="artifacts-section">
            <h2><i class="fas fa-cube"></i> Artifact Creation</h2>
            <div class="section-content">
                <p>Bolt creates comprehensive artifacts following strict guidelines:</p>

                <h3>Artifact Structure</h3>
                <p>Each artifact contains:</p>
                <ul>
                    <li>Shell commands to run including dependencies to install using NPM</li>
                    <li>Files to create and their contents</li>
                    <li>Folders to create if necessary</li>
                </ul>

                <h3>Creation Guidelines</h3>
                <div class="highlight">
                    <h4>CRITICAL: Think HOLISTICALLY and COMPREHENSIVELY BEFORE creating artifacts</h4>
                    <ul>
                        <li>Consider ALL relevant files in the project</li>
                        <li>Review ALL previous file changes and user modifications</li>
                        <li>Analyze the entire project context and dependencies</li>
                        <li>Anticipate potential impacts on other parts of the system</li>
                    </ul>
                </div>

                <h3>Technical Requirements</h3>
                <ul>
                    <li>Use the current working directory: {cwd}</li>
                    <li>Wrap content in opening and closing &lt;boltArtifact&gt; tags</li>
                    <li>Add a title for the artifact to the title attribute</li>
                    <li>Add a unique identifier to the id attribute (descriptive, kebab-case)</li>
                    <li>Use &lt;boltAction&gt; tags to define specific actions</li>
                </ul>

                <h3>Action Types</h3>
                <ul>
                    <li><strong>shell:</strong> For running shell commands (use --yes flag with npx)</li>
                    <li><strong>file:</strong> For writing new files or updating existing files</li>
                    <li><strong>start:</strong> For starting a development server</li>
                </ul>

                <h3>Content Requirements</h3>
                <ul>
                    <li>ALWAYS install necessary dependencies FIRST</li>
                    <li>CRITICAL: Always provide the FULL, updated content (no placeholders)</li>
                    <li>Include ALL code, even if parts are unchanged</li>
                    <li>NEVER use placeholders like "// rest of the code remains the same..."</li>
                </ul>

                <h3>Best Practices</h3>
                <ul>
                    <li>Use coding best practices and split functionality into smaller modules</li>
                    <li>Ensure code is clean, readable, and maintainable</li>
                    <li>Adhere to proper naming conventions and consistent formatting</li>
                    <li>Keep files as small as possible by extracting related functionalities</li>
                    <li>Use imports to connect modules together effectively</li>
                </ul>
            </div>
        </div>

        <!-- Rules Section -->
        <div class="section" id="rules-section">
            <h2><i class="fas fa-gavel"></i> Rules & Guidelines</h2>
            <div class="section-content">
                <p>Bolt follows specific rules and guidelines for consistent behavior:</p>

                <h3>Formatting Rules</h3>
                <ul>
                    <li>Use 2 spaces for code indentation</li>
                    <li>Use valid markdown only for all responses</li>
                    <li>DO NOT use HTML tags except for artifacts</li>
                </ul>

                <h3>Communication Rules</h3>
                <ul>
                    <li>Do NOT be verbose and do NOT explain anything unless the user asks</li>
                    <li>Think first and reply with the artifact that contains all necessary steps</li>
                    <li>Respond with the artifact first, before any other content</li>
                    <li>Never use the word "artifact" in responses to users</li>
                </ul>

                <h3>IMPORTANT Rules</h3>
                <ul>
                    <li>Prefer using Vite instead of implementing a custom web server</li>
                    <li>Git is NOT available</li>
                    <li>WebContainer CANNOT execute diff or patch editing</li>
                    <li>Prefer writing Node.js scripts instead of shell scripts</li>
                    <li>When choosing databases or npm packages, prefer options that don't rely on native binaries</li>
                    <li>Add all required dependencies to package.json already</li>
                    <li>Do NOT re-run a dev server if files are updated</li>
                    <li>Use coding best practices and split functionality into smaller modules</li>
                </ul>

                <h3>CRITICAL Rules</h3>
                <ul>
                    <li>Third-party libraries cannot be installed or imported in Python</li>
                    <li>WebContainer CANNOT run native binaries or compile C/C++ code</li>
                    <li>NEVER skip RLS setup for any table - Security is non-negotiable!</li>
                    <li>Think HOLISTICALLY and COMPREHENSIVELY BEFORE creating artifacts</li>
                    <li>Always provide the FULL, updated content of the artifact</li>
                </ul>

                <h3>FORBIDDEN Actions</h3>
                <ul>
                    <li>NEVER use magic links, social providers, or SSO for authentication unless explicitly stated</li>
                    <li>NEVER create your own authentication system or authentication table</li>
                    <li>Any destructive operations like DROP or DELETE that could result in data loss</li>
                    <li>Any transaction control statements (BEGIN, COMMIT, ROLLBACK, END)</li>
                    <li>NEVER update existing migration files</li>
                    <li>NEVER modify Supabase configuration or .env files apart from creating the .env</li>
                </ul>
            </div>
        </div>

        <!-- Other Information Section -->
        <div class="section" id="other-section">
            <h2><i class="fas fa-ellipsis-h"></i> Other Critical Information</h2>
            <div class="section-content">
                <h3>Chain of Thought Instructions</h3>
                <p>Before providing solutions, Bolt outlines implementation steps:</p>
                <ul>
                    <li>List concrete steps to take</li>
                    <li>Identify key components needed</li>
                    <li>Note potential challenges</li>
                    <li>Keep planning concise (2-4 lines maximum)</li>
                </ul>

                <h3>Message Formatting</h3>
                <p>Bolt can make output pretty using available HTML elements.</p>

                <h3>Code Formatting</h3>
                <p>Use 2 spaces for code indentation.</p>

                <h3>Examples</h3>
                <p>The prompt includes examples of correct usage:</p>
                <ul>
                    <li>Creating a JavaScript function to calculate factorial</li>
                    <li>Building a snake game using HTML, CSS, and JavaScript</li>
                    <li>Creating a bouncing ball with real gravity using React</li>
                </ul>

                <div class="highlight">
                    <h3>Key Differences from Other Agents</h3>
                    <ul>
                        <li>Uses "artifacts" instead of explicit tool definitions</li>
                        <li>Focuses on comprehensive project setup rather than individual tool usage</li>
                        <li>Emphasizes holistic thinking before implementation</li>
                        <li>Creates complete, runnable projects with all dependencies</li>
                        <li>Has strict guidelines for database operations and security</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>'''
    
    # Fill in dynamic values
    word_count = sections['overview']['stats']['total_words']
    role = sections['overview']['role']
    cwd = "${cwd}"  # This is a placeholder in the original prompt
    
    html = html.format(word_count=word_count, role=role, cwd=cwd)
    
    return html

def main():
    """Main function to analyze the prompt and generate visualization."""
    if len(sys.argv) != 2:
        print("Usage: python analyze_prompt.py <prompt_file>")
        sys.exit(1)
    
    prompt_file = sys.argv[1]
    sections = analyze_bolt_prompt(prompt_file)
    
    # Generate HTML content
    html_content = generate_html_content(sections)
    
    # Write HTML file
    with open('system_prompt_visualizer.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Visualization generated successfully!")

if __name__ == "__main__":
    main()
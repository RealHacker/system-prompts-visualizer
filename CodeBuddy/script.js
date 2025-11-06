// DOM Elements
const navLinks = document.querySelectorAll('.nav-link');
const contentSections = document.querySelectorAll('.content-section');

// Tool data from our analysis
const toolsData = [
    {
        name: "chat_mode_respond",
        description: "Respond to the user's inquiry with a conversational reply. Used in CHAT MODE for engaging in natural conversation, answering questions, and discussing topics.",
        parameters: [
            {
                name: "response",
                description: "The response to provide to the user. Do not try to use tools in this parameter.",
                required: true
            },
            {
                name: "path",
                description: "File path string indicating the source file of code included in response. Required only when a single code block is present.",
                required: false
            }
        ]
    },
    {
        name: "read_file",
        description: "Request to read the contents of a file at the specified path. Use to examine existing files for analysis, review, or information extraction.",
        parameters: [
            {
                name: "path",
                description: "The path of the file to read (relative to the current working directory).",
                required: true
            }
        ]
    },
    {
        name: "search_files",
        description: "Request to perform a regex search across files in a specified directory, providing context-rich results.",
        parameters: [
            {
                name: "path",
                description: "The path of the directory to search in (relative to the current working directory). This directory will be recursively searched.",
                required: true
            },
            {
                name: "regex",
                description: "The regular expression pattern to search for. Uses Rust regex syntax.",
                required: true
            },
            {
                name: "file_pattern",
                description: "Glob pattern to filter files (e.g., '*.ts' for TypeScript files). If not provided, it will search all files (*).",
                required: false
            }
        ]
    },
    {
        name: "list_files",
        description: "Request to list files and directories within the specified directory. Can list recursively or top-level only.",
        parameters: [
            {
                name: "path",
                description: "The path of the directory to list contents for (relative to the current working directory).",
                required: true
            },
            {
                name: "recursive",
                description: "Whether to list files recursively. Use true for recursive listing, false or omit for top-level only.",
                required: false
            }
        ]
    },
    {
        name: "list_code_definition_names",
        description: "Request to list definition names (classes, functions, methods, etc.) used in source code files at the top level of the specified directory.",
        parameters: [
            {
                name: "path",
                description: "The path of the directory to list top level source code definitions for.",
                required: true
            }
        ]
    },
    {
        name: "attempt_completion",
        description: "Confirm that the task is complete. Additionally, determine if the current project requires integration with Supabase.",
        parameters: [
            {
                name: "options",
                description: "A JSON list containing integration names. If workspace includes web project or html, add relevant integration names.",
                required: false
            }
        ]
    },
    {
        name: "execute_command",
        description: "Request to execute a CLI command on the system. Use for system operations or running specific commands to accomplish tasks.",
        parameters: [
            {
                name: "command",
                description: "The CLI command to execute. Should be valid for the current operating system.",
                required: true
            },
            {
                name: "requires_approval",
                description: "Boolean indicating whether this command requires explicit user approval before execution.",
                required: true
            }
        ]
    },
    {
        name: "write_to_file",
        description: "Request to write content to a file at the specified path. If file exists, it will be overwritten; if not, it will be created.",
        parameters: [
            {
                name: "path",
                description: "The path of the file to write to (relative to the current working directory).",
                required: true
            },
            {
                name: "content",
                description: "The content to write to the file. ALWAYS provide the COMPLETE intended content.",
                required: true
            }
        ]
    },
    {
        name: "replace_in_file",
        description: "Request to replace sections of content in an existing file using SEARCH/REPLACE blocks.",
        parameters: [
            {
                name: "path",
                description: "The path of the file to modify (relative to the current working directory).",
                required: true
            },
            {
                name: "diff",
                description: "One or more SEARCH/REPLACE blocks defining exact changes to specific parts of the file.",
                required: true
            }
        ]
    },
    {
        name: "preview_markdown",
        description: "Request to preview a Markdown file by converting it to HTML and opening it in the default web browser.",
        parameters: [
            {
                name: "path",
                description: "The path of the Markdown file to preview (relative to the current working directory).",
                required: true
            }
        ]
    },
    {
        name: "openweb",
        description: "Use to start or preview a specified web address. Requires starting an available server for the HTML file.",
        parameters: [
            {
                name: "url",
                description: "The URL to open in the web browser. Must be a valid web address.",
                required: true
            }
        ]
    },
    {
        name: "ask_followup_question",
        description: "Ask the user a question to gather additional information needed to complete the task.",
        parameters: [
            {
                name: "question",
                description: "The question to ask the user. Should be clear and specific.",
                required: true
            },
            {
                name: "options",
                description: "An array of 2-5 options for the user to choose from.",
                required: false
            }
        ]
    },
    {
        name: "use_rule",
        description: "Use a rule from a file and return the rule's name and the rule's body.",
        parameters: [
            {
                name: "content",
                description: "The description of rule in Rule Description.",
                required: true
            }
        ]
    },
    {
        name: "use_mcp_tool",
        description: "Request to use a tool provided by a connected MCP server.",
        parameters: [
            {
                name: "server_name",
                description: "The name of the MCP server providing the tool.",
                required: true
            },
            {
                name: "tool_name",
                description: "The name of the tool to execute.",
                required: true
            },
            {
                name: "arguments",
                description: "A JSON object containing the tool's input parameters.",
                required: true
            }
        ]
    },
    {
        name: "access_mcp_resource",
        description: "Request to access a resource provided by a connected MCP server.",
        parameters: [
            {
                name: "server_name",
                description: "The name of the MCP server providing the resource.",
                required: true
            },
            {
                name: "uri",
                description: "The URI identifying the specific resource to access.",
                required: true
            }
        ]
    }
];

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Set up navigation
    setupNavigation();
    
    // Render tools
    renderTools();
    
    // Set up smooth scrolling
    setupSmoothScrolling();
});

// Set up navigation functionality
function setupNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get target section
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            // Update active states
            navLinks.forEach(nav => nav.classList.remove('active'));
            contentSections.forEach(section => section.classList.remove('active'));
            
            // Activate current elements
            this.classList.add('active');
            targetSection.classList.add('active');
            
            // Scroll to top of section
            targetSection.scrollIntoView({ behavior: 'smooth' });
        });
    });
}

// Render tools dynamically
function renderTools() {
    const toolsContainer = document.getElementById('tools-container');
    
    toolsData.forEach(tool => {
        const toolCard = document.createElement('div');
        toolCard.className = 'tool-card';
        
        // Create parameter HTML
        let parametersHTML = '';
        if (tool.parameters && tool.parameters.length > 0) {
            parametersHTML = `
                <div class="tool-parameters">
                    <h4>Parameters</h4>
                    ${tool.parameters.map(param => `
                        <div class="parameter-item">
                            <div class="parameter-name">
                                ${param.name}
                                ${param.required ? '<span class="required">REQUIRED</span>' : ''}
                            </div>
                            <div class="parameter-desc">${param.description}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        toolCard.innerHTML = `
            <h3><i class="fas fa-toolbox"></i> ${tool.name}</h3>
            <p>${tool.description}</p>
            ${parametersHTML}
        `;
        
        toolsContainer.appendChild(toolCard);
    });
}

// Set up smooth scrolling for anchor links
function setupSmoothScrolling() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add scroll effect to sidebar
window.addEventListener('scroll', function() {
    const sidebar = document.querySelector('.sidebar');
    if (window.scrollY > 50) {
        sidebar.style.boxShadow = '3px 0 15px rgba(0, 0, 0, 0.15)';
    } else {
        sidebar.style.boxShadow = '3px 0 10px rgba(0, 0, 0, 0.1)';
    }
});

// Add animation to cards on scroll
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animated');
        }
    });
}, observerOptions);

document.querySelectorAll('.card, .tool-card').forEach(card => {
    observer.observe(card);
});
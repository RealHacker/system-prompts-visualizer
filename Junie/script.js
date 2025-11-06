// JavaScript for Junie System Prompt Visualization
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.section');
    
    // Set first section as active by default
    if (sections.length > 0) {
        sections[0].classList.add('active');
    }
    
    // Add click event to navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get target section
            const targetId = this.getAttribute('href').substring(1);
            
            // Update active nav link
            navLinks.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            
            // Show target section and hide others
            sections.forEach(section => {
                if (section.id === targetId) {
                    section.classList.add('active');
                } else {
                    section.classList.remove('active');
                }
            });
            
            // Scroll to top of content
            document.querySelector('.main-content').scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
    
    // Load data from JSON files
    loadAnalysisData();
    
    // Initialize tooltips if any
    initializeTooltips();
});

function loadAnalysisData() {
    // Load prompt analysis data
    fetch('prompt_analysis.json')
        .then(response => response.json())
        .then(data => {
            populateOverview(data.overview);
            populateTools(data.tools);
            populateWorkflow(data.workflow);
            populateRules(data.rules);
            populateContextManagement(data.context_management);
        })
        .catch(error => {
            console.error('Error loading prompt analysis:', error);
        });
    
    // Load word count data
    fetch('word_count.json')
        .then(response => response.json())
        .then(data => {
            updateWordCountStats(data);
        })
        .catch(error => {
            console.error('Error loading word count data:', error);
        });
}

function populateOverview(overview) {
    if (!overview) return;
    
    const overviewContent = document.getElementById('overview-content');
    if (!overviewContent) return;
    
    // Update role description
    const roleElement = document.getElementById('agent-role');
    if (roleElement) {
        roleElement.textContent = overview.role || 'Not specified';
    }
    
    // Update format
    const formatElement = document.getElementById('prompt-format');
    if (formatElement) {
        formatElement.textContent = overview.format || 'Not specified';
    }
    
    // Update context window
    const contextElement = document.getElementById('context-window');
    if (contextElement) {
        contextElement.textContent = overview.context_window_limit || 'Not specified';
    }
}

function populateTools(tools) {
    if (!tools || tools.length === 0) return;
    
    const toolsContainer = document.getElementById('tools-container');
    if (!toolsContainer) return;
    
    // Clear existing content
    toolsContainer.innerHTML = '';
    
    // Add each tool
    tools.forEach(tool => {
        const toolCard = createToolCard(tool);
        toolsContainer.appendChild(toolCard);
    });
}

function createToolCard(tool) {
    const card = document.createElement('div');
    card.className = 'card tool-card';
    
    card.innerHTML = `
        <div class="card-header">
            <h3><i class="fas fa-toolbox"></i> ${tool.name}</h3>
            <span class="badge badge-primary">Tool</span>
        </div>
        <div class="card-content">
            <div class="tool-signature">${tool.signature}</div>
            <p>${tool.description}</p>
            
            ${tool.arguments && tool.arguments.length > 0 ? `
            <h4>Arguments:</h4>
            <table class="arguments-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Required</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    ${tool.arguments.map(arg => `
                    <tr>
                        <td><span class="code-inline">${arg.name}</span></td>
                        <td>${arg.required ? '<span class="badge badge-success">Required</span>' : '<span class="badge">Optional</span>'}</td>
                        <td>${arg.description}</td>
                    </tr>
                    `).join('')}
                </tbody>
            </table>
            ` : ''}
            
            ${tool.examples && tool.examples.length > 0 ? `
            <h4>Examples:</h4>
            <ul class="examples-list">
                ${tool.examples.map(example => `<li>${example}</li>`).join('')}
            </ul>
            ` : ''}
        </div>
    `;
    
    return card;
}

function populateWorkflow(workflow) {
    if (!workflow || workflow.length === 0) return;
    
    const workflowList = document.getElementById('workflow-list');
    if (!workflowList) return;
    
    workflowList.innerHTML = workflow.map(step => `<li>${step}</li>`).join('');
}

function populateRules(rules) {
    if (!rules || rules.length === 0) return;
    
    const rulesList = document.getElementById('rules-list');
    if (!rulesList) return;
    
    rulesList.innerHTML = rules.map(rule => `<li>${rule}</li>`).join('');
}

function populateContextManagement(context) {
    if (!context) return;
    
    const contextContent = document.getElementById('context-content');
    if (!contextContent) return;
    
    contextContent.innerHTML = `
        <p><strong>Context Policy:</strong> ${context.context_policy || 'Not specified'}</p>
        <p><strong>Eviction Policy:</strong> ${context.eviction_policy || 'Not specified'}</p>
        <p><strong>Memory System:</strong> ${context.memory_system || 'Not specified'}</p>
    `;
}

function updateWordCountStats(stats) {
    if (!stats) return;
    
    // Update word count
    const wordCountElement = document.getElementById('word-count');
    if (wordCountElement) {
        wordCountElement.textContent = stats.word_count || 0;
    }
    
    // Update character count
    const charCountElement = document.getElementById('char-count');
    if (charCountElement) {
        charCountElement.textContent = stats.character_count || 0;
    }
    
    // Update tool count
    const toolCountElement = document.getElementById('tool-count');
    if (toolCountElement) {
        toolCountElement.textContent = stats.tool_count || 0;
    }
}

function initializeTooltips() {
    // Add any tooltip initialization code here if needed
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
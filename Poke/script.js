// Section navigation
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function() {
        // Remove active class from all items
        document.querySelectorAll('.menu-item').forEach(i => {
            i.classList.remove('active');
        });
        
        // Add active class to clicked item
        this.classList.add('active');
        
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Show the selected section
        const sectionId = this.getAttribute('data-section') + '-section';
        document.getElementById(sectionId).classList.add('active');
    });
});

// Mobile menu toggle
document.getElementById('menuToggle').addEventListener('click', function() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
});

// Load data from JSON and populate the visualization
async function loadData() {
    try {
        const response = await fetch('prompt_analysis.json');
        const data = await response.json();
        
        // Populate stats
        document.getElementById('totalWords').textContent = data.prompt_analysis.total_words.toLocaleString();
        document.getElementById('toolCount').textContent = data.prompt_analysis.tool_count;
        document.getElementById('format').textContent = data.prompt_analysis.format;
        
        // Populate overview section
        if (data.prompt_analysis.sections.Overview) {
            document.getElementById('overview-content').textContent = data.prompt_analysis.sections.Overview.content;
            
            const keyPointsList = document.getElementById('overview-key-points');
            keyPointsList.innerHTML = '';
            data.prompt_analysis.sections.Overview.key_points.forEach(point => {
                const li = document.createElement('li');
                li.textContent = point;
                keyPointsList.appendChild(li);
            });
        }
        
        // Populate workflow section
        const workflowStepsList = document.getElementById('workflow-steps');
        workflowStepsList.innerHTML = '';
        data.workflow_steps.forEach(step => {
            const li = document.createElement('li');
            li.textContent = step;
            workflowStepsList.appendChild(li);
        });
        
        // Populate tools section
        const toolsGrid = document.getElementById('tools-grid');
        toolsGrid.innerHTML = '';
        data.tools_info.forEach(tool => {
            const toolCard = document.createElement('div');
            toolCard.className = 'tool-card';
            toolCard.innerHTML = `
                <h4><i class="fas fa-toolbox"></i> ${tool.name}</h4>
                <p>${tool.description}</p>
            `;
            toolsGrid.appendChild(toolCard);
        });
        
        // Populate context management section
        if (data.prompt_analysis.sections['Context Management']) {
            document.getElementById('context-content').textContent = data.prompt_analysis.sections['Context Management'].content;
            
            const contextKeyPointsList = document.getElementById('context-key-points');
            contextKeyPointsList.innerHTML = '';
            data.prompt_analysis.sections['Context Management'].key_points.forEach(point => {
                const li = document.createElement('li');
                li.textContent = point;
                contextKeyPointsList.appendChild(li);
            });
        }
        
        // Populate rules section
        const rulesList = document.getElementById('rules-list');
        rulesList.innerHTML = '';
        data.rules.forEach(rule => {
            const li = document.createElement('li');
            li.textContent = rule;
            rulesList.appendChild(li);
        });
        
        // Populate coding standards section
        if (data.prompt_analysis.sections['Coding Standards']) {
            document.getElementById('coding-content').textContent = data.prompt_analysis.sections['Coding Standards'].content;
            
            const codingKeyPointsList = document.getElementById('coding-key-points');
            codingKeyPointsList.innerHTML = '';
            data.prompt_analysis.sections['Coding Standards'].key_points.forEach(point => {
                const li = document.createElement('li');
                li.textContent = point;
                codingKeyPointsList.appendChild(li);
            });
        }
        
        // Populate other information section
        const toolsDetails = document.getElementById('tools-details');
        toolsDetails.innerHTML = '';
        data.tools_info.forEach(tool => {
            const toolDetail = document.createElement('div');
            toolDetail.className = 'tool-detail';
            toolDetail.innerHTML = `
                <h4>${tool.name}</h4>
                <p>${tool.description}</p>
            `;
            toolsDetails.appendChild(toolDetail);
        });
        
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Initialize visualization when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});
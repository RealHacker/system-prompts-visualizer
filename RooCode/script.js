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
    const isCollapsed = sidebar.style.width === '70px';
    
    if (isCollapsed) {
        sidebar.style.width = '280px';
        document.querySelector('.main-content').style.marginLeft = '280px';
        
        // Show text labels
        document.querySelector('.sidebar-header h1 span').style.display = 'inline';
        document.querySelectorAll('.menu-item span').forEach(span => {
            span.style.display = 'inline';
        });
    } else {
        sidebar.style.width = '70px';
        document.querySelector('.main-content').style.marginLeft = '70px';
        
        // Hide text labels
        document.querySelector('.sidebar-header h1 span').style.display = 'none';
        document.querySelectorAll('.menu-item span').forEach(span => {
            span.style.display = 'none';
        });
    }
});

// Generate word count visualization
function generateWordCountVisualization() {
    // Section data with word counts and colors
    const sections = [
        { name: 'Creating an MCP Server', words: 2837, color: '#4361ee', percentage: 44.5 },
        { name: 'Tool Use Guidelines', words: 460, color: '#3f37c9', percentage: 7.2 },
        { name: 'apply_diff', words: 320, color: '#4895ef', percentage: 5.0 },
        { name: 'attempt_completion', words: 315, color: '#4cc9f0', percentage: 4.9 },
        { name: 'Introduction', words: 448, color: '#f72585', percentage: 7.0 },
        { name: 'execute_command', words: 224, color: '#e63946', percentage: 3.5 },
        { name: 'write_to_file', words: 212, color: '#7209b7', percentage: 3.3 },
        { name: 'ask_followup_question', words: 210, color: '#560bad', percentage: 3.3 },
        { name: 'search_and_replace', words: 196, color: '#3a0ca3', percentage: 3.1 },
        { name: 'read_file', words: 277, color: '#25a18e', percentage: 4.3 },
        { name: 'list_files', words: 136, color: '#06d6a0', percentage: 2.1 },
        { name: 'search_files', words: 127, color: '#ff9e00', percentage: 2.0 },
        { name: 'list_code_definition_names', words: 120, color: '#ef476f', percentage: 1.9 },
        { name: 'switch_mode', words: 84, color: '#ffd166', percentage: 1.3 },
        { name: 'use_mcp_tool', words: 93, color: '#073b4c', percentage: 1.5 },
        { name: 'access_mcp_resource', words: 75, color: '#118ab2', percentage: 1.2 },
        { name: 'new_task', words: 89, color: '#06d6a0', percentage: 1.4 },
        { name: 'fetch_instructions', words: 34, color: '#ff9e00', percentage: 0.5 },
        { name: 'Connected MCP Servers', words: 29, color: '#ef476f', percentage: 0.5 },
        { name: 'Rules from c:\\Projects\\JustGains-Admin\\.roo\\rules-code\\rules.md:', words: 28, color: '#ffd166', percentage: 0.4 }
    ];
    
    // Create dots (10x10 grid = 100 dots representing 100%)
    const dotGrid = document.getElementById('dotGrid');
    let dotIndex = 0;
    for (let i = 0; i < 100; i++) {
        const dot = document.createElement('div');
        dot.className = 'dot';
        dotGrid.appendChild(dot);
    }
    
    const dots = dotGrid.querySelectorAll('.dot');
    
    // Color the dots based on section percentages
    let currentIndex = 0;
    sections.forEach(section => {
        const count = Math.round(section.percentage);
        for (let i = 0; i < count && currentIndex < 100; i++) {
            dots[currentIndex].style.backgroundColor = section.color;
            currentIndex++;
        }
    });
    
    // Fill remaining dots with default color if needed
    for (let i = currentIndex; i < 100; i++) {
        dots[i].style.backgroundColor = '#e9ecef';
    }
    
    // Create legend
    const legend = document.getElementById('legend');
    sections.forEach(section => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        legendItem.innerHTML = `
            <div class="legend-color" style="background-color: ${section.color}"></div>
            <span>${section.name} (${section.percentage}%)</span>
        `;
        legend.appendChild(legendItem);
    });
}

// Initialize visualization when page loads
document.addEventListener('DOMContentLoaded', function() {
    generateWordCountVisualization();
});
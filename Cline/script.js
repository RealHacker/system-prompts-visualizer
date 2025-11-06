// Initialize Mermaid
mermaid.initialize({ startOnLoad: true });

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

// Generate word count visualization
function generateWordCountVisualization() {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    // Section data with word counts and colors (based on the analysis)
    const sections = [
        { name: 'Overview', words: 21, color: '#4361ee', percentage: 0.3 },
        { name: 'Tools Detail', words: 2612, color: '#3f37c9', percentage: 37.2 },
        { name: 'Tool Examples', words: 125, color: '#4895ef', percentage: 1.8 },
        { name: 'Tool Guidelines', words: 390, color: '#4cc9f0', percentage: 5.5 },
        { name: 'Workflow', words: 200, color: '#f72585', percentage: 2.8 },
        { name: 'Rules', words: 200, color: '#e63946', percentage: 2.8 },
        { name: 'Editing Files', words: 300, color: '#7209b7', percentage: 4.3 },
        { name: 'MCP Servers', words: 150, color: '#560bad', percentage: 2.1 },
        { name: 'Act vs Plan Mode', words: 180, color: '#3a0ca3', percentage: 2.6 },
        { name: 'Capabilities', words: 200, color: '#4cc9f0', percentage: 2.8 },
        { name: 'Other Info', words: 200, color: '#f72585', percentage: 2.8 }
    ];
    
    // Create dots (10x10 grid = 100 dots representing 100%)
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
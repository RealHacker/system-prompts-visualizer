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
    sidebar.style.width = sidebar.style.width === '70px' ? '280px' : '70px';
});

// Generate word count visualization
function generateWordCountVisualization() {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    // Section data with word counts and colors (based on actual analysis)
    const sections = [
        { name: 'Overview', words: 132, color: '#4361ee', percentage: 3.4 },
        { name: 'Personality', words: 51, color: '#3f37c9', percentage: 1.3 },
        { name: 'Planning', words: 355, color: '#4895ef', percentage: 9.1 },
        { name: 'Task Execution', words: 392, color: '#4cc9f0', percentage: 10.0 },
        { name: 'Testing', words: 237, color: '#f72585', percentage: 6.0 },
        { name: 'Sandbox & Approvals', words: 543, color: '#e63946', percentage: 13.9 },
        { name: 'Ambition vs Precision', words: 144, color: '#7209b7', percentage: 3.7 },
        { name: 'Progress Updates', words: 193, color: '#560bad', percentage: 4.9 },
        { name: 'Presenting Work', words: 307, color: '#3a0ca3', percentage: 7.8 },
        { name: 'Shell Commands', words: 93, color: '#4cc9f0', percentage: 2.4 },
        { name: 'Apply Patch', words: 365, color: '#f72585', percentage: 9.3 },
        { name: 'Update Plan', words: 116, color: '#e63946', percentage: 3.0 }
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

// Update stats from JSON data
function updateStats() {
    // In a real implementation, this would fetch from word_count.json
    // For now, we'll use the hardcoded values
    document.getElementById('totalWords').textContent = '3,920';
    document.getElementById('toolsCount').textContent = '3';
}

// Initialize visualization when page loads
document.addEventListener('DOMContentLoaded', function() {
    generateWordCountVisualization();
    updateStats();
});
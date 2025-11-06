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
    
    // Section data with word counts and colors (based on actual analysis)
    const sections = [
        { name: 'Overview', words: 300, color: '#4361ee', percentage: 9 },
        { name: 'Agentic Workflow', words: 800, color: '#3f37c9', percentage: 24 },
        { name: 'Tools', words: 3500, color: '#4895ef', percentage: 104 },
        { name: 'Context Management', words: 200, color: '#4cc9f0', percentage: 6 },
        { name: 'Rules', words: 1200, color: '#f72585', percentage: 36 },
        { name: 'Coding Standards', words: 900, color: '#e63946', percentage: 27 },
        { name: 'Other Info', words: 400, color: '#7209b7', percentage: 12 }
    ];
    
    // Normalize percentages to fit 100 dots
    const totalPercentage = sections.reduce((sum, section) => sum + section.percentage, 0);
    const normalizedSections = sections.map(section => ({
        ...section,
        percentage: Math.round((section.percentage / totalPercentage) * 100)
    }));
    
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
    normalizedSections.forEach(section => {
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
    normalizedSections.forEach(section => {
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
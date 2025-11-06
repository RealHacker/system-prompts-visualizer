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
    
    // Section data with word counts and colors
    const sections = [
        { name: 'Overview', words: 181, color: '#4361ee', percentage: 9.3 },
        { name: 'Communication', words: 136, color: '#3f37c9', percentage: 7.0 },
        { name: 'Search And Reading', words: 62, color: '#4895ef', percentage: 3.2 },
        { name: 'Making Code Changes', words: 382, color: '#4cc9f0', percentage: 19.7 },
        { name: 'Debugging', words: 52, color: '#f72585', percentage: 2.7 },
        { name: 'Calling External Apis', words: 111, color: '#e63946', percentage: 5.7 },
        { name: 'Web Citation Guideline', words: 24, color: '#7209b7', percentage: 1.2 },
        { name: 'Code Reference Guideline', words: 384, color: '#560bad', percentage: 19.8 },
        { name: 'Toolcall Guidelines', words: 257, color: '#3a0ca3', percentage: 13.2 },
        { name: 'Task States and Management', words: 175, color: '#4cc9f0', percentage: 9.0 },
        { name: 'Examples', words: 48, color: '#f72585', percentage: 2.5 },
        { name: 'Reasoning', words: 38, color: '#e63946', percentage: 2.0 }
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
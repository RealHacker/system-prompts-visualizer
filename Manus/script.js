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
    
    // Toggle visibility of text in sidebar
    const textElements = document.querySelectorAll('.sidebar-header h1 span, .menu-item span');
    textElements.forEach(el => {
        el.style.display = el.style.display === 'none' ? '' : 'none';
    });
});

// Generate word count visualization
function generateWordCountVisualization() {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    if (!dotGrid || !legend) return;
    
    // Section data with word counts and colors
    const sections = [
        { name: 'Overview', words: 37, color: '#4361ee', percentage: 1.0 },
        { name: 'General Capabilities', words: 110, color: '#3f37c9', percentage: 2.9 },
        { name: 'Tools & Interfaces', words: 188, color: '#4895ef', percentage: 4.9 },
        { name: 'Programming', words: 60, color: '#4cc9f0', percentage: 1.6 },
        { name: 'Methodology', words: 89, color: '#f72585', percentage: 2.3 },
        { name: 'Limitations', words: 70, color: '#e63946', percentage: 1.8 },
        { name: 'Prompting Guide', words: 250, color: '#7209b7', percentage: 7.5 },
        { name: 'About Manus', words: 286, color: '#560bad', percentage: 8.6 },
        { name: 'Modules', words: 1247, color: '#4cc9f0', percentage: 32.6 },
        { name: 'Agent Loop', words: 322, color: '#f72585', percentage: 8.4 },
        { name: 'Tools', words: 503, color: '#f72585', percentage: 13.1 }
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

// Format JSON for display
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}

// Initialize visualization when page loads
document.addEventListener('DOMContentLoaded', function() {
    generateWordCountVisualization();
});
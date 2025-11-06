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
    
    // Section data with word counts and colors
    const sections = [
        { name: 'Tools', words: 733, color: '#10b981', percentage: 29.9 },
        { name: 'Task Completion', words: 211, color: '#059669', percentage: 8.6 },
        { name: 'Version Control', words: 219, color: '#34d399', percentage: 8.9 },
        { name: 'Output Formatting', words: 173, color: '#4ade80', percentage: 7.1 },
        { name: 'Secrets Handling', words: 175, color: '#f59e0b', percentage: 7.1 },
        { name: 'Running Commands', words: 209, color: '#ef4444', percentage: 8.5 },
        { name: 'Large Files', words: 122, color: '#64748b', percentage: 5.0 },
        { name: 'Coding', words: 156, color: '#0ea5e9', percentage: 6.4 },
        { name: 'External Context', words: 117, color: '#8b5cf6', percentage: 4.8 },
        { name: 'Task Handling', words: 166, color: '#ec4899', percentage: 6.8 },
        { name: 'Question Handling', words: 51, color: '#f97316', percentage: 2.1 },
        { name: 'Other', words: 121, color: '#a8a29e', percentage: 4.9 }
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
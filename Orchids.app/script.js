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
    
    // Toggle text visibility
    const headerText = document.querySelector('.sidebar-header h1 span');
    const menuTexts = document.querySelectorAll('.menu-item span');
    
    if (sidebar.style.width === '280px') {
        if (headerText) headerText.style.display = 'inline';
        menuTexts.forEach(text => text.style.display = 'inline');
    } else {
        if (headerText) headerText.style.display = 'none';
        menuTexts.forEach(text => text.style.display = 'none');
    }
});

// Generate word count visualization
function generateWordCountVisualization() {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    // Section data with word counts and colors
    const sections = [
        { name: 'Decision Prompt', words: 1035, color: '#4361ee', percentage: 11.1 },
        { name: 'System Prompt', words: 8326, color: '#3f37c9', percentage: 88.9 }
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
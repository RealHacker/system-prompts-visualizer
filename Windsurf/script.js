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
    if (window.innerWidth <= 480) {
        sidebar.classList.toggle('active');
    } else {
        sidebar.style.width = sidebar.style.width === '70px' ? '280px' : '70px';
    }
});

// Generate word count visualization
function generateWordCountVisualization(sectionsData) {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    // Clear existing content
    dotGrid.innerHTML = '';
    legend.innerHTML = '';
    
    // Create dots (10x10 grid = 100 dots representing 100%)
    for (let i = 0; i < 100; i++) {
        const dot = document.createElement('div');
        dot.className = 'dot';
        dotGrid.appendChild(dot);
    }
    
    const dots = dotGrid.querySelectorAll('.dot');
    
    // Color the dots based on section percentages
    let currentIndex = 0;
    sectionsData.forEach(section => {
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
    sectionsData.forEach(section => {
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
    // This data would typically be generated dynamically
    // For now, we'll use placeholder data
    const sectionsData = [
        { name: 'Overview', words: 150, color: '#6a11cb', percentage: 25 },
        { name: 'Tool Calling', words: 200, color: '#2575fc', percentage: 33 },
        { name: 'Making Changes', words: 100, color: '#4361ee', percentage: 17 },
        { name: 'Memory System', words: 80, color: '#4895ef', percentage: 13 },
        { name: 'Code Research', words: 70, color: '#4cc9f0', percentage: 12 }
    ];
    
    generateWordCountVisualization(sectionsData);
});
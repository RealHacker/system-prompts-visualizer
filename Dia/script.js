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
    const headerSpan = document.querySelector('.sidebar-header h1 span');
    const menuSpans = document.querySelectorAll('.menu-item span');
    
    if (sidebar.style.width === '280px') {
        headerSpan.style.display = 'inline';
        menuSpans.forEach(span => span.style.display = 'inline');
    } else {
        headerSpan.style.display = 'none';
        menuSpans.forEach(span => span.style.display = 'none');
    }
});

// Generate word count visualization
function generateWordCountVisualization() {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    // Section data with word counts and colors
    const sections = [
        { name: 'General Instructions', words: 135, color: '#4361ee', percentage: 5.0 },
        { name: 'Ask Dia Hyperlinks', words: 146, color: '#3f37c9', percentage: 5.4 },
        { name: 'Media', words: 354, color: '#4895ef', percentage: 13.1 },
        { name: 'Writing Assistance', words: 253, color: '#4cc9f0', percentage: 9.4 },
        { name: 'Formulas & Equations', words: 230, color: '#f72585', percentage: 8.5 },
        { name: 'Response Formatting', words: 86, color: '#e63946', percentage: 3.2 },
        { name: 'Videos', words: 160, color: '#7209b7', percentage: 5.9 },
        { name: 'Simple Answer', words: 185, color: '#560bad', percentage: 6.9 },
        { name: 'Tables', words: 92, color: '#4cc9f0', percentage: 3.4 },
        { name: 'Voice & Tone', words: 114, color: '#f72585', percentage: 4.2 },
        { name: 'Other', words: 948, color: '#6c757d', percentage: 35.2 }
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
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
    if (sidebar.style.width === '280px') {
        document.querySelector('.sidebar-header h1 span').style.display = 'inline';
        document.querySelectorAll('.menu-item span').forEach(span => {
            span.style.display = 'inline';
        });
    } else {
        document.querySelector('.sidebar-header h1 span').style.display = 'none';
        document.querySelectorAll('.menu-item span').forEach(span => {
            span.style.display = 'none';
        });
    }
});

// Generate word count visualization
function generateWordCountVisualization() {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    // Section data with word counts and colors (accurate distribution for Same.dev)
    const sections = [
        { name: 'Overview', words: 252, color: '#0066cc', percentage: 9.8 },
        { name: 'Service Policies', words: 182, color: '#003366', percentage: 7.1 },
        { name: 'Communication', words: 158, color: '#4895ef', percentage: 6.2 },
        { name: 'Tool Calling', words: 287, color: '#4cc9f0', percentage: 11.2 },
        { name: 'Parallel Tool Calls', words: 185, color: '#f72585', percentage: 7.2 },
        { name: 'Memos', words: 155, color: '#e63946', percentage: 6.1 },
        { name: 'Making Code Changes', words: 323, color: '#7209b7', percentage: 12.6 },
        { name: 'Web Development', words: 399, color: '#560bad', percentage: 15.6 },
        { name: 'Web Design', words: 232, color: '#3f37c9', percentage: 9.1 },
        { name: 'Debugging', words: 54, color: '#4361ee', percentage: 2.1 },
        { name: 'Website Cloning', words: 200, color: '#4895ef', percentage: 7.8 },
        { name: 'Task Agent', words: 132, color: '#4cc9f0', percentage: 5.2 }
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
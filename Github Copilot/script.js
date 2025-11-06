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
    
    // Section data with word counts and colors (based on the analysis)
    const sections = [
        { name: 'Identity', words: 71, color: '#4361ee', percentage: 1.0 },
        { name: 'Instructions', words: 14, color: '#3f37c9', percentage: 0.2 },
        { name: 'Tool Use', words: 549, color: '#4895ef', percentage: 8.0 },
        { name: 'Edit File', words: 273, color: '#4cc9f0', percentage: 4.0 },
        { name: 'Functions', words: 1815, color: '#f72585', percentage: 26.5 },
        { name: 'Context', words: 13, color: '#e63946', percentage: 0.2 },
        { name: 'Reminder', words: 23, color: '#7209b7', percentage: 0.3 },
        { name: 'Apply Patch', words: 542, color: '#560bad', percentage: 7.9 },
        { name: 'Todo List', words: 150, color: '#3a0ca3', percentage: 2.2 },
        { name: 'Notebook', words: 130, color: '#4cc9f0', percentage: 1.9 },
        { name: 'Output Format', words: 355, color: '#f72585', percentage: 5.2 },
        { name: 'Environment', words: 40, color: '#e63946', percentage: 0.6 },
        { name: 'Workspace', words: 81, color: '#7209b7', percentage: 1.2 },
        { name: 'Editor Context', words: 6, color: '#560bad', percentage: 0.1 },
        { name: 'Reminder Instructions', words: 465, color: '#3a0ca3', percentage: 6.8 },
        { name: 'User Request', words: 18, color: '#4361ee', percentage: 0.3 }
    ];
    
    // Calculate total words for percentage calculation
    const totalWords = sections.reduce((sum, section) => sum + section.words, 0);
    
    // Update percentages
    sections.forEach(section => {
        section.percentage = (section.words / totalWords * 100);
    });
    
    // Sort sections by percentage (descending)
    sections.sort((a, b) => b.percentage - a.percentage);
    
    // Take top 10 sections for visualization
    const topSections = sections.slice(0, 10);
    
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
    topSections.forEach(section => {
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
    topSections.forEach(section => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        legendItem.innerHTML = `
            <div class="legend-color" style="background-color: ${section.color}"></div>
            <span>${section.name} (${section.percentage.toFixed(1)}%)</span>
        `;
        legend.appendChild(legendItem);
    });
}

// Initialize visualization when page loads
document.addEventListener('DOMContentLoaded', function() {
    generateWordCountVisualization();
});
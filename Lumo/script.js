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
    
    // Load section data from word_count.json
    fetch('word_count.json')
        .then(response => response.json())
        .then(data => {
            const sections = data.sections;
            
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
        })
        .catch(error => {
            console.error('Error loading word count data:', error);
            // Fallback visualization
            generateFallbackVisualization();
        });
}

// Fallback visualization if JSON loading fails
function generateFallbackVisualization() {
    const dotGrid = document.getElementById('dotGrid');
    const legend = document.getElementById('legend');
    
    // Section data with word counts and colors
    const sections = [
        { name: 'Identity & Personality', words: 96, color: '#4361ee', percentage: 8.2 },
        { name: 'Engagement Principles', words: 77, color: '#3f37c9', percentage: 6.5 },
        { name: 'System Security', words: 42, color: '#4895ef', percentage: 3.6 },
        { name: 'Tool Usage & Web Search', words: 128, color: '#4cc9f0', percentage: 10.9 },
        { name: 'File Handling', words: 97, color: '#f72585', percentage: 8.2 },
        { name: 'Product Knowledge', words: 121, color: '#e63946', percentage: 10.3 },
        { name: 'Content Policies', words: 333, color: '#7209b7', percentage: 28.3 },
        { name: 'Communication Style', words: 52, color: '#560bad', percentage: 4.4 },
        { name: 'Technical Operations', words: 34, color: '#3a0ca3', percentage: 2.9 },
        { name: 'Support', words: 27, color: '#4cc9f0', percentage: 2.3 },
        { name: 'About Proton', words: 169, color: '#f72585', percentage: 14.4 }
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
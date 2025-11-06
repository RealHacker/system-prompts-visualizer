// Mobile menu toggle
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.querySelector('.sidebar');

menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

// Section navigation
const menuItems = document.querySelectorAll('.menu-item');
const sections = document.querySelectorAll('.section');

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        // Remove active class from all items and sections
        menuItems.forEach(i => i.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));
        
        // Add active class to clicked item
        item.classList.add('active');
        
        // Show corresponding section
        const sectionId = item.getAttribute('data-section') + '-section';
        document.getElementById(sectionId).classList.add('active');
        
        // Close sidebar on mobile after selection
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
        }
    });
});

// Initialize Mermaid
mermaid.initialize({ startOnLoad: true });

// Function to update stats (would be called by analysis script)
function updateStats(totalWords, toolCount) {
    document.getElementById('totalWords').textContent = totalWords.toLocaleString();
    document.getElementById('toolCount').textContent = toolCount;
}

// Simulate loading data (in a real implementation, this would come from the analysis script)
document.addEventListener('DOMContentLoaded', function() {
    // These values would normally be populated by running the analysis script
    updateStats(15700, 6); // Approximate values for Kiro spec prompt
});
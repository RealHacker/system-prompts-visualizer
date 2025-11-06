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
    sidebar.classList.toggle('active');
});

// Update stats with actual values
document.addEventListener('DOMContentLoaded', function() {
    // These values would typically be populated dynamically
    // For now, we'll use placeholder values
    document.getElementById('totalWords').textContent = '15,200';
    document.getElementById('toolCount').textContent = '15';
    document.getElementById('contextWindow').textContent = 'Not specified';
});
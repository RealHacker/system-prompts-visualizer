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

// Update stats with actual values (in a real implementation, these would be populated dynamically)
document.addEventListener('DOMContentLoaded', function() {
    // These values would typically be populated dynamically by analyzing the prompt
    // For now, we'll use placeholder values
    document.getElementById('totalWords').textContent = '5,553';
    document.getElementById('toolCount').textContent = '41';
    document.getElementById('contextWindow').textContent = 'Not specified';
    document.getElementById('agentRole').textContent = 'Devin is a software engineer AI agent designed to work with users on engineering tasks using a real computer operating system.';
});
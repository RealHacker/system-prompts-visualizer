// JavaScript for Perplexity System Prompt Visualization
document.addEventListener('DOMContentLoaded', function() {
    // Load sections when the page loads
    loadSections();
    
    // Add event listeners to sidebar items
    const sidebarItems = document.querySelectorAll('.sidebar li');
    sidebarItems.forEach(item => {
        item.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);
        });
    });
});

function loadSections() {
    // Show the first section by default
    showSection('overview');
}

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Show the selected section
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.add('active');
    }
    
    // Update active state in sidebar
    const sidebarItems = document.querySelectorAll('.sidebar li');
    sidebarItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-section') === sectionId) {
            item.classList.add('active');
        }
    });
    
    // Scroll to top of content
    document.querySelector('.content').scrollTo(0, 0);
}
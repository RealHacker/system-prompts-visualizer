// Additional JavaScript functionality for Cluely visualization
// This file can be used to extend the embedded scripts in the HTML file

document.addEventListener('DOMContentLoaded', function() {
    // Update statistics dynamically
    updateStatistics();
    
    // Add any additional event listeners
    addEventListeners();
});

function updateStatistics() {
    // This function would typically fetch real data from an analysis
    // For now, we'll use the values we determined from our analysis
    
    // These values are based on our analysis of the prompt files
    document.getElementById('totalWords').textContent = '3,083';
    document.getElementById('toolCount').textContent = '0';
    document.getElementById('contextWindow').textContent = 'Not specified';
}

function addEventListeners() {
    // Add any additional event listeners here
    // For example, search functionality, export options, etc.
    
    // Example: Add a print button functionality
    const printButton = document.createElement('button');
    printButton.innerHTML = '<i class="fas fa-print"></i> Print';
    printButton.className = 'theme-toggle';
    printButton.style.right = '70px';
    printButton.addEventListener('click', function() {
        window.print();
    });
    
    // Only add the print button if we're not in a mobile view
    if (window.innerWidth > 768) {
        document.body.appendChild(printButton);
    }
}

// Export functionality for saving the visualization
function exportAsHTML() {
    const htmlContent = document.documentElement.outerHTML;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'cluely_system_prompt_visualization.html';
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
}

// Function to search within the document
function searchContent(query) {
    // This would implement search functionality across the sections
    // For now, we'll just log the query
    console.log('Search query:', query);
    
    // In a full implementation, this would:
    // 1. Search through all section content
    // 2. Highlight matching terms
    // 3. Scroll to the first match
    // 4. Show search results
}

// Make functions available globally
window.exportAsHTML = exportAsHTML;
window.searchContent = searchContent;
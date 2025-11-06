document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const toggleThemeButton = document.getElementById('toggle-theme');
    const body = document.body;
    
    // Check for saved theme preference or respect OS preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        body.classList.add('dark-mode');
    }
    
    toggleThemeButton.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        
        // Save theme preference
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Update active nav link
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
                
                // Scroll to target
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Set active nav link based on scroll position
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    function updateActiveLink() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveLink);
    
    // Initialize active link
    updateActiveLink();
    
    // Tool parameter expand/collapse functionality
    const toolCards = document.querySelectorAll('.tool-card');
    toolCards.forEach(card => {
        const paramsHeader = card.querySelector('h4');
        if (paramsHeader) {
            paramsHeader.style.cursor = 'pointer';
            paramsHeader.addEventListener('click', function() {
                const paramsContent = this.nextElementSibling;
                if (paramsContent.style.display === 'none') {
                    paramsContent.style.display = 'block';
                    this.textContent = this.textContent.replace('▶', '▼');
                } else {
                    paramsContent.style.display = 'none';
                    this.textContent = this.textContent.replace('▼', '▶');
                }
            });
        }
    });
});
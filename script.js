// Landing Page Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // Video toggle functionality
    const videoLinks = document.querySelectorAll('a[href^="#video-"]');
    
    videoLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const videoContainer = document.querySelector(targetId);
            
            if (videoContainer) {
                // Toggle display
                if (videoContainer.style.display === 'none' || videoContainer.style.display === '') {
                    videoContainer.style.display = 'block';
                    this.textContent = 'Hide Video';
                } else {
                    videoContainer.style.display = 'none';
                    this.textContent = 'Demo Video';
                }
            }
        });
    });

    // Smooth scroll with offset for sticky nav
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            // Skip if it's a video toggle link
            if (href.startsWith('#video-')) {
                return;
            }
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const navHeight = document.querySelector('.main-nav').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all module cards
    document.querySelectorAll('.module-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(card);
    });

    // Highlight active navigation
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.main-nav a');

    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            const navHeight = document.querySelector('.main-nav').offsetHeight;
            
            if (window.pageYOffset >= sectionTop - navHeight - 100) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // Add a status indicator for module links
    checkModuleAvailability();
});

// Check if module pages are accessible
function checkModuleAvailability() {
    const moduleLinks = document.querySelectorAll('.btn-primary[href^="assignment"]');
    
    moduleLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Add a visual indicator that links are ready
        link.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.4)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
}

// Console greeting
console.log('%cComputer Vision Portfolio', 'font-size: 20px; color: #2563eb; font-weight: bold;');
console.log('%cAll modules are ready for demonstration!', 'font-size: 14px; color: #64748b;');
console.log('Modules: Perspective Measurement | Template Matching | Image Analysis | Panorama | SAM2 | Stereo Vision');


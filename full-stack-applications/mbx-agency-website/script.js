// Mobile Navigation Toggle
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
    });
});

// Smooth scrolling for navigation links
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Header background change on scroll
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.98)';
        header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.boxShadow = 'none';
    }
});

// Modal functionality
function openModal() {
    const modal = document.getElementById('contactModal');
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('contactModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('contactModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// Form submission
document.querySelector('.contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    // Simple validation
    if (!data.name || !data.email) {
        alert('Por favor, preencha os campos obrigatórios.');
        return;
    }
    
    // Simulate form submission
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    submitBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        alert('Mensagem enviada com sucesso! Entraremos em contato em breve.');
        this.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        closeModal();
    }, 2000);
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.service-card, .result-card, .about-item');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Counter animation for results
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Animate counters when they come into view
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counter = entry.target.querySelector('.result-number');
            if (counter && !counter.dataset.animated) {
                const text = counter.textContent;
                const number = parseInt(text.replace(/[^0-9]/g, ''));
                const sign = text.includes('+') ? '+' : text.includes('-') ? '-' : '';
                
                counter.dataset.animated = 'true';
                counter.textContent = '0';
                
                setTimeout(() => {
                    animateCounter(counter, number);
                    setTimeout(() => {
                        counter.textContent = sign + number;
                    }, 2000);
                }, 500);
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.result-card').forEach(card => {
    counterObserver.observe(card);
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroGraphic = document.querySelector('.hero-graphic');
    
    if (heroGraphic) {
        heroGraphic.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Smooth reveal animation for sections
const revealSections = document.querySelectorAll('.services, .results, .about, .cta-section');

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
        }
    });
}, { threshold: 0.1 });

revealSections.forEach(section => {
    revealObserver.observe(section);
});

// Add CSS for reveal animation
const style = document.createElement('style');
style.textContent = `
    .services, .results, .about, .cta-section {
        opacity: 0;
        transform: translateY(50px);
        transition: opacity 0.8s ease, transform 0.8s ease;
    }
    
    .services.revealed, .results.revealed, .about.revealed, .cta-section.revealed {
        opacity: 1;
        transform: translateY(0);
    }
    
    body.loaded .hero {
        animation: fadeInUp 1s ease;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Add hover effects for service cards
document.querySelectorAll('.service-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Add typing effect for hero title
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typing effect when page loads
function initializeHeroTitle() {
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        // Clear the title initially to prevent showing HTML tags
        heroTitle.innerHTML = '';
        
        // Start typing effect after a delay
        setTimeout(() => {
            const textContent = 'Muito além de uma agência comum';
            let currentText = '';
            let i = 0;
            
            function typeWithHTML() {
                if (i < textContent.length) {
                    currentText += textContent.charAt(i);
                    
                    // Reconstruct HTML with highlight
                    if (currentText.includes('agência comum')) {
                        const beforeHighlight = currentText.split('agência comum')[0];
                        heroTitle.innerHTML = beforeHighlight + '<span class="highlight">agência comum</span>';
                    } else {
                        heroTitle.innerHTML = currentText;
                    }
                    
                    i++;
                    setTimeout(typeWithHTML, 50);
                }
            }
            
            typeWithHTML();
        }, 1000);
    }
}

// Try multiple event listeners to ensure it works
document.addEventListener('DOMContentLoaded', initializeHeroTitle);
window.addEventListener('load', initializeHeroTitle);

// Also try immediately if DOM is already ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeHeroTitle);
} else {
    initializeHeroTitle();
}

// Add scroll progress indicator
const progressBar = document.createElement('div');
progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    z-index: 9999;
    transition: width 0.3s ease;
`;
document.body.appendChild(progressBar);

window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset;
    const docHeight = document.body.offsetHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    progressBar.style.width = scrollPercent + '%';
});

// Add floating action button for WhatsApp
const whatsappBtn = document.createElement('a');
whatsappBtn.href = 'https://wa.me/5541998358844?text=Olá! Gostaria de saber mais sobre os serviços da MBX Agency.';
whatsappBtn.target = '_blank';
whatsappBtn.innerHTML = '<i class="fab fa-whatsapp"></i>';
whatsappBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: #25d366;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    text-decoration: none;
    box-shadow: 0 4px 20px rgba(37, 211, 102, 0.3);
    z-index: 1000;
    transition: all 0.3s ease;
`;

whatsappBtn.addEventListener('mouseenter', function() {
    this.style.transform = 'scale(1.1)';
    this.style.boxShadow = '0 6px 25px rgba(37, 211, 102, 0.4)';
});

whatsappBtn.addEventListener('mouseleave', function() {
    this.style.transform = 'scale(1)';
    this.style.boxShadow = '0 4px 20px rgba(37, 211, 102, 0.3)';
});

document.body.appendChild(whatsappBtn);

// Add back to top button
const backToTopBtn = document.createElement('button');
backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopBtn.style.cssText = `
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: none;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    z-index: 1000;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
`;

backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

backToTopBtn.addEventListener('mouseenter', function() {
    this.style.transform = 'scale(1.1)';
});

backToTopBtn.addEventListener('mouseleave', function() {
    this.style.transform = 'scale(1)';
});

document.body.appendChild(backToTopBtn);

// Show/hide back to top button
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopBtn.style.display = 'flex';
    } else {
        backToTopBtn.style.display = 'none';
    }
});

console.log('MBX Agency website loaded successfully! 🚀'); 
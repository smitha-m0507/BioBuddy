// Smooth scrolling for navigation links
document.querySelectorAll('a.nav-link').forEach(link => {
    link.addEventListener('click', event => {
        // Prevent default anchor behavior
        event.preventDefault();

        // Get the target section's ID from the href attribute
        const targetId = link.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);

        if (targetSection) {
            // Scroll smoothly to the target section
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        }
    });
});

// Basic animation on scroll: Fade-in effect
const sections = document.querySelectorAll('section');

const observer = new IntersectionObserver(
    (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.2 }
);

sections.forEach(section => {
    section.classList.add('hidden');
    observer.observe(section);
});

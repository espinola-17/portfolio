// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Scroll reveal
const revealElements = document.querySelectorAll('.reveal');

const revealOnScroll = () => {
    const windowHeight = window.innerHeight;
    revealElements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const revealPoint = 100;
        
        if (elementTop < windowHeight - revealPoint) {
            element.classList.add('active');
        }
    });
};

window.addEventListener('scroll', revealOnScroll);
revealOnScroll();

// Fetch GitHub projects
async function fetchGitHubProjects() {
    const container = document.getElementById('github-projects');
    
    try {
        const response = await fetch('/api/github-projects');
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Failed to fetch projects');
        }
        
        container.innerHTML = '';
        
        if (data.projects.length === 0) {
            container.innerHTML = `
                <div class="project-card" style="text-align: center; padding: 3rem; grid-column: 1/-1;">
                    <p style="color: var(--text-secondary);">No public repositories found. Start building amazing projects!</p>
                </div>
            `;
            return;
        }
        
        data.projects.forEach(project => {
            const projectCard = document.createElement('div');
            projectCard.className = 'project-card reveal';
            
            projectCard.innerHTML = `
                <div class="project-header">
                    <h3 class="project-title">${escapeHtml(project.name)}</h3>
                    <p class="project-description">${escapeHtml(project.description)}</p>
                </div>
                <div class="project-footer">
                    <div class="project-tech">
                        ${project.language ? `<span class="tech-tag">${escapeHtml(project.language)}</span>` : ''}
                        ${project.stars > 0 ? `<span class="tech-tag">⭐ ${project.stars}</span>` : ''}
                    </div>
                    <a href="${escapeHtml(project.url)}" class="project-link" target="_blank" rel="noopener">View →</a>
                </div>
            `;
            
            container.appendChild(projectCard);
        });
        
        revealOnScroll();
        
    } catch (error) {
        console.error('Error fetching GitHub projects:', error);
        container.innerHTML = `
            <div class="project-card" style="text-align: center; padding: 3rem; grid-column: 1/-1;">
                <p style="color: var(--text-secondary);">Unable to load projects. Please try again later.</p>
            </div>
        `;
    }
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

window.addEventListener('load', fetchGitHubProjects);

// Active nav link
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (window.scrollY >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.style.color = '';
        if (link.getAttribute('href') === `#${current}`) {
            link.style.color = 'var(--accent-cyan)';
        }
    });
});

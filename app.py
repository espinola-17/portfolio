"""
Portfolio Web Application
Built with Flask to demonstrate Python web development skills
"""
from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Configuration and Credentials
app.config['GITHUB_USERNAME'] = os.getenv('GITHUB_USERNAME', 'espinola-17')
app.config['EMAIL'] = 'enrico@enricospinola.com'
app.config['LINKEDIN'] = 'spinolajrenrico'

# Portfolio data 
SKILLS = {
    'Cloud & Infrastructure': ['AWS', 'Azure', 'Oracle', 'Docker'],
    'Programming': ['Python', 'SQL', 'Bash', 'JavaScript', 'HTML/CSS'],
    'Data & Analytics': ['Power BI', 'Tableau', 'MySQL', 'Oracle', 'PostgreSQL'],
    'DevOps & Tools': ['Git', 'CI/CD', 'Virtual Machines']
}

# About Section
ABOUT = {
    'title': 'Cloud & Systems Engineer',
    'bio': '''Entry-level engineer passionate about building scalable infrastructure and automating workflows. 
    Strong foundation in cloud platforms, containerization, and data analysis. 
    Currently seeking opportunities in DevOps, Systems Engineering, or Data Analytics roles.''',
    'experience_years': '5+',
    'projects_count': '10+',
    'certifications': ['Coming Soon']
}

# Projects Sections
PROJECTS = [
    {
        'title': 'Enterprise Work Tracking System',
        'tech': ['SharePoint', 'Power Apps', 'Power Automate', 'Java', 'Oracle'],
        'description': 'Modernized work tracking and request management system at financial services company',
        'highlights': [
            'Led migration from legacy SharePoint 2016 to SharePoint Online',
            'Designed automated approval workflows reducing manual routing delays',
            'System success influenced organization to redevelop as Java-based enterprise application',
            'Collaborated with development teams during enterprise platform transition'
        ]
    },
    {
        'title': 'Executive Dashboard & BI Platform',
        'tech': ['Power BI', 'Oracle', 'SharePoint', 'SQL'],
        'description': 'Operational dashboards providing KPIs and insights for leadership',
        'highlights': [
            'Built Power BI dashboards connecting SharePoint and Oracle databases',
            'Evolved data architecture from SharePoint lists to Oracle database',
            'Designed visualizations highlighting operational issues and performance metrics',
            'Enabled data-driven decision making across multiple departments'
        ]
    },
    {
        'title': 'Self-Hosted Portfolio Infrastructure',
        'tech': ['Python', 'Flask', 'Linux', 'Cloudflare Tunnel', 'systemd', 'MySQL'],
        'description': 'Production web application on Dell R510 home server',
        'highlights': [
            'Built Flask application with MySQL database integration',
            'Configured systemd service for automatic restart and monitoring',
            'Secured with Cloudflare zero-trust tunnel (no open ports)',
            'Integrated GitHub API for dynamic project display'
        ]
    },
    {
        'title': 'Cloud Infrastructure Lab',
        'tech': ['Oracle Cloud', 'Azure', 'Docker', 'CI/CD'],
        'description': 'Personal cloud environment for learning and experimentation',
        'highlights': [
            'Deployed Docker containers on Oracle Cloud free tier',
            'Configured Azure DevOps pipelines for automated deployments',
            'Managed Linux VMs and networking configurations',
            'Experimented with infrastructure-as-code concepts'
        ]
    }
]

# Resume Download
RESUME = {
    'file': 'Resume_DevOps.pdf',
    'filename': 'Enrico_Spinola_Resume.pdf'
}

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html', 
                         about=ABOUT,
                         skills=SKILLS,
                         projects=PROJECTS,
                         resume=RESUME,
                         github_username=app.config['GITHUB_USERNAME'],
                         email=app.config['EMAIL'],
                         linkedin=app.config['LINKEDIN'])

@app.route('/api/github-projects')
def github_projects():
    """API endpoint to fetch GitHub projects"""
    username = app.config['GITHUB_USERNAME']
    
    try:
        response = requests.get(
            f'https://api.github.com/users/{username}/repos',
            params={'sort': 'updated', 'per_page': 6},
            timeout=5
        )
        
        if response.status_code == 200:
            repos = response.json()
            projects = []
            for repo in repos:
                if not repo['fork']:
                    projects.append({
                        'name': repo['name'],
                        'description': repo['description'] or 'No description provided',
                        'url': repo['html_url'],
                        'language': repo['language'],
                        'stars': repo['stargazers_count'],
                        'updated': repo['updated_at']
                    })
            
            projects.sort(key=lambda x: x['stars'], reverse=True)
            
            return jsonify({
                'success': True,
                'projects': projects[:6]
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch repositories'
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'portfolio-app'
    })

if __name__ == '__main__':
    # For development only - systemd uses gunicorn instead
    import os
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

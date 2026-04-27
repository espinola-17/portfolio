"""
Portfolio Web Application
Built with Flask to demonstrate Python web development skills
"""
from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Configuration - UPDATE THESE WITH YOUR INFO!
app.config['GITHUB_USERNAME'] = os.getenv('GITHUB_USERNAME', 'espinola-17')
app.config['EMAIL'] = 'enrico@enricospinola.com'
app.config['LINKEDIN'] = 'spinolajrenrico'

# Portfolio data - UPDATE WITH YOUR ACTUAL SKILLS!
SKILLS = {
    'Cloud & Infrastructure': ['AWS', 'Azure', 'Docker'],
    'Programming': ['Python', 'SQL', 'Bash', 'JavaScript', 'HTML/CSS'],
    'Data & Analytics': ['Power BI', 'Tableau', 'MySQL', 'Oracle', 'PostgreSQL'],
    'DevOps & Tools': ['Git', 'CI/CD', 'Virtual Machines']
}

# UPDATE WITH YOUR INFO!
ABOUT = {
    'title': 'Cloud & Systems Engineer',
    'bio': '''Entry-level engineer passionate about building scalable infrastructure and automating workflows. 
    Strong foundation in cloud platforms, containerization, and data analysis. 
    Currently seeking opportunities in DevOps, Systems Engineering, or Data Analytics roles.''',
    'experience_years': '1+',
    'projects_count': '10+',
    'certifications': ['Coming Soon']
}

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html', 
                         about=ABOUT,
                         skills=SKILLS,
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

# Portfolio Website

My professional portfolio showcasing projects, skills, and experience in DevOps, Systems Engineering, and Data Analytics.

🌐 **Live Site:** [enricospinola.com](https://enricospinola.com)

## 🚀 Features

- **Dynamic GitHub Integration** - Automatically displays latest projects via GitHub API
- **Modern Responsive Design** - Works on desktop, tablet, and mobile
- **Self-Hosted Infrastructure** - Runs on my Dell R510 home server
- **Production-Ready** - Systemd service with auto-restart and logging
- **Secure Access** - Cloudflare Tunnel for zero-trust network access

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Systemd service on Ubuntu Server
- **Networking:** Cloudflare Tunnel
- **Version Control:** Git/GitHub
- **Process Manager:** Gunicorn WSGI server

## 📋 Architecture

┌─────────────────┐
│   Public Web    │
│ enricospinola.  │
│      com        │
└────────┬────────┘
│
│ HTTPS
▼
┌─────────────────┐
│   Cloudflare    │
│     Tunnel      │
└────────┬────────┘
│
│ Encrypted
▼
┌─────────────────┐
│  Dell R510      │
│  Home Server    │
│                 │
│  ┌───────────┐  │
│  │ Systemd   │  │
│  │ Service   │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ Gunicorn  │  │
│  │  :5777    │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │   Flask   │  │
│  │    App    │  │
│  └───────────┘  │
└─────────────────┘

## 🏗️ Project Structure
portfolio/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── main.js       # Frontend JavaScript
└── README.md             # This file

## 🔧 Local Development

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/espinola-17/portfolio.git
cd portfolio

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py
```

Visit `http://localhost:5000`

## 🚀 Production Deployment

This portfolio runs as a systemd service on my home server. Here's the deployment process:

### 1. Create systemd service

```bash
sudo nano /etc/systemd/system/portfolio.service
```

```ini
[Unit]
Description=Portfolio Web Application
After=network.target

[Service]
Type=simple
User=your-user
Group=your-group
WorkingDirectory=/path/to/portfolio
Environment="PATH=/path/to/portfolio/venv/bin"
Environment="GITHUB_USERNAME=your-github-username"
ExecStart=/path/to/portfolio/venv/bin/gunicorn --bind 0.0.0.0:5777 --workers 2 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Enable and start service

```bash
sudo systemctl daemon-reload
sudo systemctl enable portfolio
sudo systemctl start portfolio
```

### 3. Configure Cloudflare Tunnel

Add to your `config.yml`:

```yaml
ingress:
  - hostname: yourdomain.com
    service: http://localhost:5777
  - service: http_status:404
```

## 🔄 Updating the Site

```bash
# Pull latest changes
cd ~/portfolio
git pull

# Restart the service
sudo systemctl restart portfolio

# Check status
sudo systemctl status portfolio
```

## 📊 API Endpoints

- `GET /` - Main portfolio page
- `GET /api/github-projects` - Returns GitHub repositories as JSON
- `GET /health` - Health check endpoint for monitoring

## 🎨 Customization

### Update Your Information

Edit `app.py` and modify:

```python
# Lines 13-15: Contact information
app.config['GITHUB_USERNAME'] = 'your-username'
app.config['EMAIL'] = 'your@email.com'
app.config['LINKEDIN'] = 'your-linkedin'

# Lines 18-23: Your skills
SKILLS = {
    'Category': ['Skill1', 'Skill2', ...],
    ...
}

# Lines 25-33: Your bio and stats
ABOUT = {
    'title': 'Your Title',
    'bio': 'Your bio...',
    ...
}
```

### Add Your Photo

1. Place your photo in `static/images/profile.jpg`
2. In `templates/index.html`, replace the emoji with:
```html
   <img src="{{ url_for('static', filename='images/profile.jpg') }}" alt="Your Name">
```

## 📝 Environment Variables

The application supports these environment variables:

- `GITHUB_USERNAME` - Your GitHub username (for API calls)
- `PORT` - Port to run on (default: 5000 for dev, configured in systemd for prod)

## 🔒 Security

- ✅ Cloudflare Tunnel provides zero-trust network access
- ✅ No ports exposed directly to the internet
- ✅ DDoS protection via Cloudflare
- ✅ Automatic SSL/TLS encryption
- ✅ Environment variables for sensitive data

## 📈 Performance

- **Workers:** 2 Gunicorn workers for concurrent requests
- **Auto-restart:** Systemd ensures service availability
- **Caching:** Static assets served efficiently
- **CDN:** Cloudflare edge network for global delivery

## 🐛 Troubleshooting

### Service not starting

```bash
# Check service status
sudo systemctl status portfolio

# View logs
sudo journalctl -u portfolio -n 50

# Common issues:
# - Wrong paths in service file
# - Missing dependencies
# - Port already in use
```

### GitHub projects not loading

- Check your GitHub username in `app.py`
- Verify you have public repositories
- Check API rate limits (60 requests/hour without auth)

### Can't access via domain

```bash
# Check Cloudflare Tunnel
sudo systemctl status cloudflared

# Verify DNS settings in Cloudflare dashboard
# Ensure CNAME points to your tunnel
```

## 📚 Learning Resources

This project demonstrates skills useful for:
- **DevOps Engineering** - Service management, deployment automation
- **Systems Engineering** - Linux administration, process management
- **Full-Stack Development** - Backend APIs, frontend design
- **Cloud/Infrastructure** - Self-hosting, networking, security

## 🤝 Contributing

This is a personal portfolio project, but feel free to:
- Fork it for your own portfolio
- Submit issues if you find bugs
- Suggest improvements via pull requests

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

**Enrico Spinola**
- 🌐 Website: [enricospinola.com](https://enricospinola.com)
- 📧 Email: enrico@enricospinola.com
- 💼 LinkedIn: [linkedin.com/in/enricospinola](https://linkedin.com/in/enricospinola)
- 💻 GitHub: [@espinola-17](https://github.com/espinola-17)

---

**Built with using Python, Flask, and self-hosted infrastructure**

*This portfolio runs on a Dell R510 home server, demonstrating real-world systems administration and DevOps practices.*

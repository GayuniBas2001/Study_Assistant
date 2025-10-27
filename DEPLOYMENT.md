# Deployment Guide

This guide covers different deployment options for the Study Assistant application.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Cloud Deployment](#cloud-deployment)

## Local Development

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed local development setup instructions.

Quick start:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env to add GEMINI_API_KEY
python main.py

# Frontend (in new terminal)
cd frontend
npm install
npm start
```

## Docker Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Quick Start with Docker Compose

1. **Clone the repository**
```bash
git clone https://github.com/GayuniBas2001/Study_Assistant.git
cd Study_Assistant
```

2. **Set up environment variables**
```bash
# Create .env file in project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

3. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

This will:
- Build both backend and frontend images
- Start both services
- Backend available at `http://localhost:8000`
- Frontend available at `http://localhost:3000`

4. **View logs**
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

5. **Stop services**
```bash
docker-compose down

# With volume cleanup
docker-compose down -v
```

### Manual Docker Build

**Backend:**
```bash
cd backend
docker build -t study-assistant-backend .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/vector_store:/app/vector_store \
  study-assistant-backend
```

**Frontend:**
```bash
cd frontend
docker build -t study-assistant-frontend .
docker run -p 3000:80 \
  -e REACT_APP_API_URL=http://localhost:8000 \
  study-assistant-frontend
```

## Production Deployment

### Prerequisites
- Production server (Ubuntu 20.04+ recommended)
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)
- Reverse proxy (Nginx recommended)

### Backend Production Setup

1. **Update server**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install Python and dependencies**
```bash
sudo apt install -y python3.11 python3.11-venv python3-pip nginx
```

3. **Set up application**
```bash
# Create app directory
sudo mkdir -p /var/www/study-assistant
cd /var/www/study-assistant

# Clone repository
git clone https://github.com/GayuniBas2001/Study_Assistant.git .

# Set up backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production values
nano .env
```

4. **Create systemd service**
```bash
sudo nano /etc/systemd/system/study-assistant-backend.service
```

Add:
```ini
[Unit]
Description=Study Assistant Backend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/study-assistant/backend
Environment="PATH=/var/www/study-assistant/backend/venv/bin"
ExecStart=/var/www/study-assistant/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable study-assistant-backend
sudo systemctl start study-assistant-backend
sudo systemctl status study-assistant-backend
```

5. **Configure Nginx reverse proxy**
```bash
sudo nano /etc/nginx/sites-available/study-assistant-backend
```

Add:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/study-assistant-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Frontend Production Setup

1. **Build frontend**
```bash
cd /var/www/study-assistant/frontend
npm install
REACT_APP_API_URL=https://api.yourdomain.com npm run build
```

2. **Configure Nginx for frontend**
```bash
sudo nano /etc/nginx/sites-available/study-assistant-frontend
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    root /var/www/study-assistant/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/study-assistant-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Setup with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Cloud Deployment

### AWS Deployment

**Using EC2:**
1. Launch EC2 instance (t2.medium recommended)
2. Follow production deployment steps above
3. Configure security groups:
   - Port 80 (HTTP)
   - Port 443 (HTTPS)
   - Port 22 (SSH)

**Using ECS with Docker:**
1. Push images to ECR
2. Create ECS cluster
3. Define task definitions
4. Create services
5. Configure Application Load Balancer

**Using Elastic Beanstalk:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 study-assistant

# Create environment
eb create study-assistant-prod

# Deploy
eb deploy
```

### Google Cloud Platform

**Using Compute Engine:**
1. Create VM instance
2. Follow production deployment steps
3. Configure firewall rules

**Using Cloud Run:**
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/study-assistant-backend backend/
gcloud builds submit --tag gcr.io/PROJECT_ID/study-assistant-frontend frontend/

# Deploy backend
gcloud run deploy study-assistant-backend \
  --image gcr.io/PROJECT_ID/study-assistant-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend
gcloud run deploy study-assistant-frontend \
  --image gcr.io/PROJECT_ID/study-assistant-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment

**Using App Service:**
```bash
# Login
az login

# Create resource group
az group create --name StudyAssistantRG --location eastus

# Create App Service plan
az appservice plan create --name StudyAssistantPlan --resource-group StudyAssistantRG --sku B1 --is-linux

# Deploy backend
az webapp create --resource-group StudyAssistantRG --plan StudyAssistantPlan --name study-assistant-backend --runtime "PYTHON:3.11"

# Deploy frontend
az webapp create --resource-group StudyAssistantRG --plan StudyAssistantPlan --name study-assistant-frontend --runtime "NODE:18-lts"
```

### Heroku Deployment

**Backend:**
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
cd backend
heroku create study-assistant-backend

# Set config
heroku config:set GEMINI_API_KEY=your_key

# Deploy
git push heroku main
```

**Frontend:**
```bash
cd frontend
heroku create study-assistant-frontend
heroku config:set REACT_APP_API_URL=https://study-assistant-backend.herokuapp.com
git push heroku main
```

## Environment Variables

### Backend
```bash
GEMINI_API_KEY=your_gemini_api_key
UPLOAD_DIR=./uploads
VECTOR_STORE_DIR=./vector_store
LOG_LEVEL=INFO
```

### Frontend
```bash
REACT_APP_API_URL=http://localhost:8000  # or production URL
```

## Monitoring

### Health Checks

Backend health endpoint:
```bash
curl http://localhost:8000/health
```

Frontend health endpoint:
```bash
curl http://localhost:3000/health
```

### Logs

**Docker:**
```bash
docker-compose logs -f
```

**Systemd:**
```bash
sudo journalctl -u study-assistant-backend -f
```

**Nginx:**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Backup and Recovery

### Backup Vector Store
```bash
# Create backup
tar -czf vector_store_backup_$(date +%Y%m%d).tar.gz backend/vector_store/

# Restore backup
tar -xzf vector_store_backup_YYYYMMDD.tar.gz -C backend/
```

### Backup Uploaded Files
```bash
# Create backup
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz backend/uploads/

# Restore backup
tar -xzf uploads_backup_YYYYMMDD.tar.gz -C backend/
```

## Scaling

### Horizontal Scaling

1. **Load Balancer Setup (Nginx)**
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

2. **Shared Storage**
- Use NFS or cloud storage for uploads
- Use managed vector database service

3. **Database for Metadata**
- Migrate to PostgreSQL for chat history
- Use Redis for caching

### Vertical Scaling

Increase resources:
- CPU: 2+ cores recommended
- RAM: 4GB+ recommended
- Storage: SSD recommended for vector store

## Troubleshooting

### Backend not starting
```bash
# Check logs
sudo journalctl -u study-assistant-backend -n 50

# Check port
sudo netstat -tulpn | grep 8000

# Verify environment
source venv/bin/activate
python -c "from config import settings; print(settings.gemini_api_key)"
```

### Frontend not building
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 16+
```

### Connection issues
```bash
# Check firewall
sudo ufw status

# Allow ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check Nginx
sudo nginx -t
sudo systemctl status nginx
```

## Security Checklist

- [ ] Use HTTPS for all connections
- [ ] Set strong API keys
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Backup data regularly
- [ ] Use secrets management service
- [ ] Implement authentication

## Performance Optimization

1. **Enable Caching**
   - Redis for API responses
   - CDN for static assets

2. **Optimize Database**
   - Index frequently queried fields
   - Use connection pooling

3. **Compress Responses**
   - Enable gzip in Nginx
   - Minify frontend assets

4. **Use CDN**
   - CloudFlare
   - AWS CloudFront
   - Google Cloud CDN

## Maintenance

### Regular Tasks

**Daily:**
- Monitor logs for errors
- Check disk space

**Weekly:**
- Review performance metrics
- Update dependencies if needed

**Monthly:**
- Backup vector store and uploads
- Security audit
- Performance optimization review

**Quarterly:**
- Update SSL certificates
- Review and update documentation
- Disaster recovery drill

## Support

For deployment issues:
1. Check logs first
2. Review documentation
3. Check GitHub issues
4. Create new issue with logs and environment details

# OpenGW Agentic Transaction Analyzer - Deployment Guide

This comprehensive guide provides step-by-step instructions for deploying the OpenGW Agentic Transaction Analyzer in various environments, from local development to production cloud deployments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Deployment](#local-development-deployment)
3. [Production Deployment Options](#production-deployment-options)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying the application, ensure you have the following requirements met:

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **Node.js**: Version 18.0 or higher
- **Python**: Version 3.11 or higher
- **Memory**: Minimum 2GB RAM (4GB recommended for production)
- **Storage**: At least 1GB free disk space

### Required Software

```bash
# Install Node.js (if not already installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.11 (if not already installed)
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev

# Install build tools
sudo apt-get install build-essential
```

## Local Development Deployment

### Quick Start

The fastest way to get the application running locally is using the provided development script:

```bash
# Extract the project archive
tar -xzf opengw-vuejs-analyzer.tar.gz
cd opengw-vuejs-analyzer

# Make scripts executable
chmod +x start-dev.sh
chmod +x build-production.sh

# Start development environment
./start-dev.sh
```

This script will automatically:
- Check port availability (8000 for backend, 5173 for frontend)
- Set up the Python virtual environment
- Install backend dependencies
- Start the FastAPI backend server
- Install frontend dependencies
- Start the Vite development server
- Enable cache prevention for both services

### Manual Development Setup

If you prefer to set up the environment manually:

#### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables for cache prevention
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Start the backend server
python main.py
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
export NODE_ENV=development
export VITE_API_BASE_URL=http://localhost:8000
export VITE_CACHE_BUSTER=$(date +%s)

# Start development server
npm run dev
```

## Production Deployment Options

### Option 1: Traditional Server Deployment

#### Step 1: Prepare the Production Build

```bash
# Run the production build script
./build-production.sh
```

This creates an optimized build with:
- Minified and hash-named assets
- Cache-busting headers
- Production-ready backend configuration

#### Step 2: Server Setup

```bash
# Install production dependencies
sudo apt-get update
sudo apt-get install nginx python3.11 python3.11-venv

# Create application directory
sudo mkdir -p /opt/opengw-analyzer
sudo chown $USER:$USER /opt/opengw-analyzer

# Extract production build
tar -xzf opengw-analyzer-*.tar.gz -C /opt/opengw-analyzer --strip-components=1
```

#### Step 3: Backend Service Configuration

Create a systemd service file:

```bash
sudo tee /etc/systemd/system/opengw-analyzer.service << EOF
[Unit]
Description=OpenGW Agentic Transaction Analyzer
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/opengw-analyzer/backend
Environment=PATH=/opt/opengw-analyzer/backend/.venv/bin
Environment=PYTHONDONTWRITEBYTECODE=1
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/opengw-analyzer/backend/.venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable opengw-analyzer
sudo systemctl start opengw-analyzer
```

#### Step 4: Nginx Configuration

```bash
sudo tee /etc/nginx/sites-available/opengw-analyzer << EOF
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain
    
    # Cache prevention headers
    add_header Cache-Control "no-cache, no-store, must-revalidate";
    add_header Pragma "no-cache";
    add_header Expires "0";
    
    # Frontend static files
    location / {
        root /opt/opengw-analyzer/frontend/dist;
        try_files \$uri \$uri/ /index.html;
        
        # Additional cache prevention for static files
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires "0";
        }
    }
    
    # Backend API proxy
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Disable proxy caching
        proxy_cache off;
        proxy_no_cache 1;
        proxy_cache_bypass 1;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/opengw-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 2: Process Manager Deployment (PM2)

```bash
# Install PM2 globally
npm install -g pm2

# Create PM2 ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [
    {
      name: 'opengw-backend',
      cwd: './backend',
      script: 'main.py',
      interpreter: '.venv/bin/python',
      env: {
        PYTHONDONTWRITEBYTECODE: '1',
        PYTHONUNBUFFERED: '1'
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    }
  ]
};
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Docker Deployment

### Create Dockerfile for Backend

```bash
cat > backend/Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables for cache prevention
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
EOF
```

### Create Dockerfile for Frontend

```bash
cat > frontend/Dockerfile << EOF
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code and build
COPY . .
ENV VITE_CACHE_BUSTER=\$(date +%s)
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration with cache prevention
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOF
```

### Create Docker Compose Configuration

```bash
cat > docker-compose.yml << EOF
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
    environment:
      - VITE_API_BASE_URL=http://backend:8000

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
EOF
```

### Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale backend if needed
docker-compose up -d --scale backend=3
```

## Cloud Deployment

### AWS Deployment (using EC2 and Application Load Balancer)

#### Step 1: Launch EC2 Instance

```bash
# Create security group
aws ec2 create-security-group \\
    --group-name opengw-analyzer-sg \\
    --description "Security group for OpenGW Analyzer"

# Add inbound rules
aws ec2 authorize-security-group-ingress \\
    --group-name opengw-analyzer-sg \\
    --protocol tcp \\
    --port 80 \\
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \\
    --group-name opengw-analyzer-sg \\
    --protocol tcp \\
    --port 443 \\
    --cidr 0.0.0.0/0

# Launch instance
aws ec2 run-instances \\
    --image-id ami-0c02fb55956c7d316 \\
    --count 1 \\
    --instance-type t3.medium \\
    --key-name your-key-pair \\
    --security-groups opengw-analyzer-sg
```

#### Step 2: Deploy Application

```bash
# SSH to instance and deploy
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt-get update
sudo apt-get install -y nginx python3.11 python3.11-venv nodejs npm

# Deploy application (follow traditional server deployment steps above)
```

### Google Cloud Platform Deployment

```bash
# Create App Engine configuration
cat > app.yaml << EOF
runtime: python311

env_variables:
  PYTHONDONTWRITEBYTECODE: "1"
  PYTHONUNBUFFERED: "1"

handlers:
- url: /api/.*
  script: auto

- url: /.*
  static_dir: frontend/dist
  upload: frontend/dist/.*
EOF

# Deploy to App Engine
gcloud app deploy
```

### Azure Deployment

```bash
# Create resource group
az group create --name opengw-analyzer-rg --location eastus

# Create App Service plan
az appservice plan create \\
    --name opengw-analyzer-plan \\
    --resource-group opengw-analyzer-rg \\
    --sku B1 \\
    --is-linux

# Create web app
az webapp create \\
    --resource-group opengw-analyzer-rg \\
    --plan opengw-analyzer-plan \\
    --name opengw-analyzer-app \\
    --runtime "PYTHON|3.11"

# Deploy code
az webapp deployment source config-zip \\
    --resource-group opengw-analyzer-rg \\
    --name opengw-analyzer-app \\
    --src opengw-analyzer-production.zip
```

## Environment Configuration

### Environment Variables

Create a `.env` file for production configuration:

```bash
cat > .env << EOF
# Application Configuration
NODE_ENV=production
PYTHON_ENV=production

# API Configuration
API_BASE_URL=https://your-domain.com/api
API_TIMEOUT=30000

# Cache Prevention
CACHE_BUSTER_ENABLED=true
FORCE_NO_CACHE=true

# Security
CORS_ORIGINS=https://your-domain.com
ALLOWED_HOSTS=your-domain.com

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance
MAX_UPLOAD_SIZE=50MB
REQUEST_TIMEOUT=30s
EOF
```

### SSL/TLS Configuration

```bash
# Install Certbot for Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Maintenance

### Health Checks

The application includes built-in health check endpoints:

```bash
# Backend health check
curl http://localhost:8000/api/health

# Expected response:
# {
#   "status": "ok",
#   "timestamp": 1234567890,
#   "version": "1.0.0"
# }
```

### Log Monitoring

```bash
# View application logs
sudo journalctl -u opengw-analyzer -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Performance Monitoring

```bash
# Install monitoring tools
sudo apt-get install htop iotop nethogs

# Monitor system resources
htop

# Monitor network usage
sudo nethogs

# Monitor disk I/O
sudo iotop
```

### Backup Strategy

```bash
# Create backup script
cat > backup.sh << EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"

# Create backup directory
mkdir -p \$BACKUP_DIR

# Backup application files
tar -czf \$BACKUP_DIR/opengw-analyzer-\$DATE.tar.gz /opt/opengw-analyzer

# Backup configuration
cp /etc/nginx/sites-available/opengw-analyzer \$BACKUP_DIR/nginx-config-\$DATE.conf
cp /etc/systemd/system/opengw-analyzer.service \$BACKUP_DIR/systemd-service-\$DATE.service

# Clean old backups (keep last 7 days)
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: \$BACKUP_DIR/opengw-analyzer-\$DATE.tar.gz"
EOF

chmod +x backup.sh

# Schedule daily backups
echo "0 2 * * * /path/to/backup.sh" | crontab -
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :5173

# Kill the process
sudo kill -9 <PID>
```

#### Issue: Permission Denied

```bash
# Fix file permissions
sudo chown -R www-data:www-data /opt/opengw-analyzer
sudo chmod -R 755 /opt/opengw-analyzer
```

#### Issue: Module Not Found (Python)

```bash
# Reinstall dependencies
cd backend
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Issue: Build Failures (Frontend)

```bash
# Clear npm cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Issue: Cache Not Prevented

Verify cache prevention is working:

```bash
# Check response headers
curl -I http://localhost:8000/api/health

# Should include:
# Cache-Control: no-cache, no-store, must-revalidate, private
# Pragma: no-cache
# Expires: 0
```

### Performance Optimization

#### Backend Optimization

```bash
# Use Gunicorn for production
pip install gunicorn

# Start with multiple workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

#### Frontend Optimization

```bash
# Enable gzip compression in Nginx
sudo tee -a /etc/nginx/sites-available/opengw-analyzer << EOF
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
EOF
```

### Security Hardening

```bash
# Install fail2ban
sudo apt-get install fail2ban

# Configure firewall
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

# Update system packages
sudo apt-get update && sudo apt-get upgrade -y
```

## Conclusion

This deployment guide provides comprehensive instructions for deploying the OpenGW Agentic Transaction Analyzer in various environments. The cache prevention strategies implemented throughout the application ensure that users always receive the most current version of both the frontend interface and backend API responses.

For additional support or questions about deployment, please refer to the project documentation or contact the development team.

---

**Author**: Manus AI  
**Last Updated**: October 2025  
**Version**: 1.0.0

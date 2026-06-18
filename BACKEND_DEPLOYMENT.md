# Backend Deployment Guide

Complete guide for deploying the Python backend with LangGraph integration.

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Database Setup](#database-setup)
5. [LLM Configuration](#llm-configuration)
6. [Monitoring & Logging](#monitoring--logging)
7. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip or conda
- SQLite3 (included in Python)
- OpenAI API key

### Step 1: Clone and Setup

```bash
git clone <repository>
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
cp .env.example .env

# Edit .env with your settings:
# - OPENAI_API_KEY=sk-your-key-here
# - DATABASE_URL=sqlite:///./analytics.db
```

### Step 4: Initialize Database

```bash
python init_db.py
# Output:
# ✓ Products: 8
# ✓ Customers: 6
# ✓ Sales: 120
```

### Step 5: Run Development Server

```bash
python main.py
# Or with auto-reload:
uvicorn main:app --reload --port 8000
```

**Access API:**
- Application: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Docker Deployment

### Using Docker Compose (Recommended)

#### Step 1: Setup Environment

```bash
cp backend/.env.example backend/.env

# Edit backend/.env:
# OPENAI_API_KEY=sk-your-key-here
```

#### Step 2: Build and Run

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
```

#### Step 3: Initialize Database

```bash
docker-compose exec backend python init_db.py
```

#### Step 4: Verify Services

```bash
# Check services
docker-compose ps

# Test API
curl http://localhost:8000/health
curl http://localhost/api/health  # through nginx
```

### Services Included

1. **Frontend** (Port 3000)
   - React application
   - Auto-rebuild on changes

2. **Backend** (Port 8000)
   - FastAPI application
   - LangGraph agent
   - Database operations

3. **PostgreSQL** (Port 5432) - Optional
   - Persistent database
   - Better for production

4. **Redis** (Port 6379) - Optional
   - Result caching
   - Session storage

5. **Nginx** (Port 80)
   - Reverse proxy
   - Load balancing
   - Static file serving

### Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Execute command in container
docker-compose exec backend python init_db.py

# Rebuild images
docker-compose build --no-cache

# Remove volumes (data will be deleted!)
docker-compose down -v
```

---

## Production Deployment

### Option 1: AWS EC2

#### Instance Setup

```bash
# Launch EC2 instance (Ubuntu 22.04)
# t3.medium or larger recommended

# SSH into instance
ssh -i key.pem ubuntu@instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Deploy Application

```bash
# Clone repository
git clone <repository> /opt/data-analyst-agent
cd /opt/data-analyst-agent

# Configure environment
sudo cp backend/.env.example backend/.env
sudo nano backend/.env  # Edit with your settings

# Start services
docker-compose up -d

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d your-domain.com
```

#### Security Groups
Configure AWS Security Group:
- Port 80 (HTTP) - from 0.0.0.0/0
- Port 443 (HTTPS) - from 0.0.0.0/0
- Port 22 (SSH) - from your IP only

#### Database Backup
```bash
# Automated daily backup
0 2 * * * docker-compose exec -T postgres pg_dump -U analyst analytics > /backups/db_$(date +\%Y\%m\%d).sql
```

### Option 2: DigitalOcean App Platform

1. **Connect Repository**
   - Go to DigitalOcean App Platform
   - Click "Create App"
   - Select GitHub repository

2. **Configure Services**
   - Frontend: Node.js, `npm run build`
   - Backend: Python, `python main.py`

3. **Set Environment Variables**
   - OPENAI_API_KEY
   - DATABASE_URL
   - LOG_LEVEL

4. **Deploy**
   - DigitalOcean handles auto-deployment on push

### Option 3: Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add environment variables
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set DATABASE_URL=postgresql://...

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 4: Kubernetes

```bash
# Create namespace
kubectl create namespace data-analyst

# Create secrets
kubectl create secret generic api-keys \
  --from-literal=openai-api-key=sk-... \
  -n data-analyst

# Deploy using helm
helm repo add data-analyst https://charts.example.com
helm install data-analyst data-analyst/agent \
  -n data-analyst \
  -f values.yaml

# Scale replicas
kubectl scale deployment backend --replicas=3 -n data-analyst
```

---

## Database Setup

### SQLite (Development)

```python
# .env
DATABASE_URL=sqlite:///./analytics.db
```

**Advantages:**
- No setup required
- Portable
- Good for development

**Limitations:**
- Single writer
- No concurrent access
- Not suitable for production

### PostgreSQL (Production Recommended)

#### Local PostgreSQL

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb analytics
sudo -u postgres createuser analyst -P

# Grant privileges
sudo -u postgres psql -c "ALTER USER analyst WITH CREATEDB;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE analytics TO analyst;"
```

#### Configuration

```env
DATABASE_URL=postgresql://analyst:password@localhost:5432/analytics
```

#### Docker PostgreSQL

```bash
# Using docker-compose (already configured)
docker-compose up -d postgres

# Initialize
docker-compose exec postgres psql -U analyst -d analytics < init_db_postgres.sql
```

#### Backup & Restore

```bash
# Backup
docker-compose exec postgres pg_dump -U analyst analytics > backup.sql

# Restore
docker-compose exec -T postgres psql -U analyst analytics < backup.sql
```

### Connection Pooling

For production, use connection pooling:

```env
# PostgreSQL with pooling
DATABASE_URL=postgresql://analyst:password@pooler.example.com:6432/analytics
```

Popular poolers:
- **PgBouncer** (lightweight)
- **PgPool-II** (advanced)
- **RDS Proxy** (AWS managed)

---

## LLM Configuration

### OpenAI Setup

1. **Get API Key**
   ```
   1. Go to https://platform.openai.com/account/api-keys
   2. Create new API key
   3. Copy key
   ```

2. **Set Environment Variable**
   ```env
   OPENAI_API_KEY=sk-proj-xxxxx...
   OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for cost savings
   ```

3. **Monitor Usage**
   ```
   View usage and costs at:
   https://platform.openai.com/account/billing/overview
   ```

### Alternative LLM Providers

#### Azure OpenAI

```env
OPENAI_API_TYPE=azure
OPENAI_API_BASE=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2024-01-15
OPENAI_API_KEY=your-key-here
```

#### Anthropic Claude

```python
# Update agent.py
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-opus-20240229")
```

#### Open Source Models

```python
# Using Ollama locally
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral")
```

### Cost Optimization

```python
# Use cheaper model for analysis
# Use GPT-4 only for complex queries

config.OPENAI_MODEL = "gpt-3.5-turbo"  # ~10x cheaper
config.LLM_TEMPERATURE = 0.0  # Deterministic results
```

---

## Monitoring & Logging

### Application Logs

```env
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

**Log Locations:**
```
- Console: Real-time output
- File: logs/app.log
- Docker: docker-compose logs -f backend
```

### Log Monitoring Tools

#### ELK Stack (Elasticsearch, Logstash, Kibana)

```yaml
# docker-compose addition
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  environment:
    - discovery.type=single-node

kibana:
  image: docker.elastic.co/kibana/kibana:8.0.0
  ports:
    - "5601:5601"
```

#### Loki + Grafana

```bash
# For log aggregation and visualization
docker run -d --name loki grafana/loki:latest
docker run -d --name grafana grafana/grafana:latest
```

### Performance Monitoring

```python
# Add to main.py
from prometheus_client import Counter, Histogram

query_counter = Counter('queries_total', 'Total queries')
query_duration = Histogram('query_duration_seconds', 'Query duration')
```

### Alerting

```bash
# Set up alerts for:
# - Error rate > 5%
# - Response time > 2 seconds
# - Database connection failures
# - API key expiration
```

---

## Troubleshooting

### Backend Won't Start

**Error: "Module not found"**
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt

# Or in Docker:
docker-compose build --no-cache
docker-compose up -d backend
```

**Error: "Database connection failed"**
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
python -c "from database import db_manager; print(db_manager.test_connection())"

# If PostgreSQL:
psql $DATABASE_URL -c "SELECT 1"
```

### OpenAI API Errors

**Error: "Invalid API key"**
```bash
# Verify key is set
echo $OPENAI_API_KEY

# Check key is valid at:
# https://platform.openai.com/account/api-keys
```

**Error: "Rate limit exceeded"**
```python
# Add retry logic
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=2, max=10))
def call_llm():
    # ...
```

### Query Execution Issues

**Error: "Query timeout"**
```env
# Increase timeout
MAX_QUERY_TIMEOUT=60

# Or optimize query to run faster
```

**Error: "Result set too large"**
```env
# Reduce limit
MAX_QUERY_LIMIT=500
```

### Docker Issues

**Container exits immediately**
```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose build --no-cache backend
```

**Port already in use**
```bash
# Find process using port
lsof -i :8000

# Use different port
docker-compose up -d -p 8001:8000 backend
```

---

## Performance Tuning

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_sales_date ON sales(date);
CREATE INDEX idx_sales_category ON products(category);
CREATE INDEX idx_sales_segment ON sales(segment);

-- Analyze tables for query planner
ANALYZE;
```

### LLM Optimization

```python
# Cache responses for identical questions
from functools import lru_cache

@lru_cache(maxsize=100)
async def generate_sql(question: str):
    # ...
```

### API Optimization

```python
# Enable response compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add caching headers
@app.get("/schema")
async def get_schema():
    response.headers["Cache-Control"] = "max-age=3600"
```

---

## Security Hardening

### Environment Variables

```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use secrets management
# AWS: AWS Secrets Manager
# GCP: Secret Manager
# Azure: Key Vault
```

### API Security

```python
# Add rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze(request):
    # ...
```

### Database Security

```sql
-- Restrict user permissions
ALTER ROLE analyst WITH NOINHERIT;
GRANT USAGE ON SCHEMA public TO analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;

-- Disable unused features
-- REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM analyst;
```

### SSL/TLS

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Configure in nginx.conf (uncomment SSL section)
```

---

## Maintenance

### Regular Tasks

- **Daily**: Check error logs
- **Weekly**: Monitor API usage and costs
- **Monthly**: Update dependencies, test disaster recovery
- **Quarterly**: Security audit, performance review

### Backup Strategy

```bash
# Daily backups
0 2 * * * docker-compose exec -T postgres pg_dump -U analyst analytics | gzip > /backups/db_$(date +\%Y\%m\%d).sql

# Keep last 30 days
find /backups -mtime +30 -delete
```

### Update Process

```bash
# Backup before updating
docker-compose down
cp -r data data.backup

# Update code
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# Verify
docker-compose ps
curl http://localhost:8000/health
```

---

## Support & Resources

- **API Documentation**: `http://your-domain/docs`
- **GitHub Issues**: Report bugs
- **OpenAI Documentation**: https://platform.openai.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **LangChain Docs**: https://python.langchain.com

---

**Deployment Status: ✅ Ready**

Complete backend implementation with production-ready deployment options.

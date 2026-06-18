# Autonomous Data Analyst Agent - Deployment Guide

## Overview

This guide provides instructions for deploying the Autonomous Data Analyst Agent in various environments.

## Local Development

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd autonomous-data-analyst

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

### Build Process

```bash
# Build the application
npm run build

# This generates:
# - dist/index.html (single-file bundle)
# - All assets inlined for easy deployment
```

### Build Output

The build process creates a single `dist/index.html` file (~645 KB gzipped) with:
- All HTML
- All CSS (Tailwind)
- All JavaScript (React + dependencies)
- No external file dependencies

### Build Optimization

```bash
# Development build
npm run dev

# Production build (optimized)
npm run build

# Preview production build locally
npm run preview
```

## Deployment Platforms

### 1. Vercel (Recommended)

**Advantages:**
- Zero-config deployment
- Automatic SSL
- Global CDN
- Free tier available

**Steps:**
```bash
# Push to GitHub
git push origin main

# Connect to Vercel
# 1. Go to vercel.com
# 2. Click "New Project"
# 3. Import from GitHub
# 4. Deploy

# Or use Vercel CLI
npm i -g vercel
vercel
```

**Configuration:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "NODE_ENV": "production"
  }
}
```

### 2. Netlify

**Advantages:**
- Simple deployment
- Good build preview
- Free tier

**Steps:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod

# Or connect via GitHub:
# 1. Push to GitHub
# 2. Connect repository in Netlify dashboard
# 3. Auto-deploy on push
```

**netlify.toml:**
```toml
[build]
  command = "npm run build"
  publish = "dist"

[dev]
  command = "npm run dev"
  port = 5173
```

### 3. GitHub Pages

**Steps:**
```bash
# Update vite.config.ts base path
# base: '/autonomous-data-analyst/'

# Build
npm run build

# Push dist folder to gh-pages branch
git subtree push --prefix dist origin gh-pages
```

**Enable in GitHub Settings:**
- Go to Settings → Pages
- Source: Deploy from branch
- Branch: gh-pages, /root

### 4. Traditional Web Hosting

**For shared hosting (cPanel, Bluehost, etc.):**

1. Build the project:
```bash
npm run build
```

2. Upload `dist/index.html` to your web server's public_html directory

3. Access via `http://yourdomain.com`

**For dedicated server (AWS, DigitalOcean, etc.):**

```bash
# Build
npm run build

# SSH to server
ssh user@server

# Copy dist to server
scp -r dist/* user@server:/var/www/html/

# Or use rsync
rsync -avz dist/ user@server:/var/www/html/
```

### 5. Docker Deployment

**Dockerfile:**
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

**Build and run:**
```bash
# Build image
docker build -t data-analyst-agent .

# Run container
docker run -p 3000:3000 data-analyst-agent

# Or use docker-compose
docker-compose up
```

**docker-compose.yml:**
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
```

## Environment Configuration

### Environment Variables

Create `.env` file for local development:
```env
VITE_APP_TITLE=Autonomous Data Analyst Agent
VITE_APP_DESCRIPTION=Ask questions about your data
VITE_API_URL=http://localhost:3000/api
VITE_ENABLE_LOGGING=true
```

Create `.env.production` for production:
```env
VITE_APP_TITLE=Autonomous Data Analyst Agent
VITE_APP_DESCRIPTION=Ask questions about your data
VITE_API_URL=https://api.example.com/api
VITE_ENABLE_LOGGING=false
```

### Access in Code

```typescript
const apiUrl = import.meta.env.VITE_API_URL
const enableLogging = import.meta.env.VITE_ENABLE_LOGGING
```

## Performance Optimization

### Code Splitting

The build automatically creates:
- `index.js` - Main bundle
- CSS - Tailwind styles
- Recharts chunks (if necessary)

### Caching Strategy

**For production servers:**

```nginx
# nginx configuration
location /dist {
    expires 1d;
    add_header Cache-Control "public, immutable";
}

location /index.html {
    expires 0;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

### Bundle Analysis

```bash
# Analyze bundle size
npm install -D rollup-plugin-analyzer

# In vite.config.ts, add analyzer plugin
```

## Monitoring & Analytics

### Google Analytics

```typescript
// Add to main.tsx
import { useEffect } from 'react'

declare global {
  interface Window {
    gtag: any
  }
}

useEffect(() => {
  const script = document.createElement('script')
  script.async = true
  script.src = `https://www.googletagmanager.com/gtag/js?id=GA_ID`
  document.head.appendChild(script)
  
  window.dataLayer = window.dataLayer || []
  function gtag() {
    window.dataLayer.push(arguments)
  }
  gtag('js', new Date())
  gtag('config', 'GA_ID')
}, [])
```

### Error Tracking (Sentry)

```typescript
// In main.tsx
import * as Sentry from "@sentry/react"

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  environment: import.meta.env.MODE,
  tracesSampleRate: 1.0,
})
```

## Security Checklist

- [ ] HTTPS enabled
- [ ] CSP headers configured
- [ ] XSS protection enabled
- [ ] CORS properly configured
- [ ] No sensitive data in frontend
- [ ] Dependencies updated
- [ ] Error messages sanitized
- [ ] SQL injection prevention (if using real DB)

### Security Headers

```nginx
# nginx headers
add_header X-Content-Type-Options "nosniff";
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()";
```

## Database Integration

### Switching from Mock to Real Database

**Step 1: Install database driver**
```bash
npm install pg  # PostgreSQL
# or
npm install mysql2  # MySQL
# or
npm install sqlite3  # SQLite
```

**Step 2: Update DataAnalystAgent**
```typescript
// Replace mock executeSQL with real query
async executeSQL(sql: string): Promise<any[]> {
  const result = await fetch('/api/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sql })
  })
  return result.json()
}
```

**Step 3: Create backend API**
```typescript
// Simple Node.js/Express backend
import express from 'express'
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
})

app.post('/api/query', async (req, res) => {
  const { sql } = req.body
  try {
    const result = await pool.query(sql)
    res.json(result.rows)
  } catch (err) {
    res.status(400).json({ error: err.message })
  }
})
```

## Scaling Considerations

### For High Traffic

1. **Use CDN** (Cloudflare, CloudFront)
   - Cache static assets
   - Global edge servers
   - DDoS protection

2. **Database Optimization**
   - Query indexing
   - Connection pooling
   - Read replicas for analytics

3. **Backend Services**
   - Separate API server
   - Load balancing
   - Query caching (Redis)

4. **Monitoring**
   - Application Performance Monitoring (APM)
   - Real User Monitoring (RUM)
   - Database metrics

## Troubleshooting Deployment

### Issue: Blank Page

**Solution:**
```bash
# Check build output
ls -la dist/

# Verify index.html exists
cat dist/index.html | head -20

# Check browser console for errors
# Verify base path in vite.config.ts
```

### Issue: Assets Not Loading

**Solution:**
```typescript
// vite.config.ts
export default {
  base: '/',  // Adjust if deployed to subdirectory
  build: {
    outDir: 'dist',
    minify: 'terser'
  }
}
```

### Issue: Slow Performance

**Solution:**
```bash
# Analyze bundle
npm run build -- --minify=false

# Check dependencies
npm list --depth=0

# Optimize images
npx imagemin src/images/* --out-dir=public/images
```

### Issue: CORS Errors

**Solution:**
If connecting to external API:
```typescript
// Use proxy in vite.config.ts
export default {
  server: {
    proxy: {
      '/api': {
        target: 'http://backend.example.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}
```

## Rollback Procedure

### Git-based Rollback
```bash
# View deployment history
git log --oneline

# Rollback to previous version
git revert <commit-hash>
git push origin main

# Redeploy
# (automatic on Vercel/Netlify)
```

### Manual Rollback
```bash
# Keep previous dist backup
cp -r dist dist.backup.$(date +%s)

# Deploy previous version
git checkout <commit-hash>
npm run build
# Upload new dist/
```

## Maintenance

### Regular Updates

```bash
# Check for updates
npm outdated

# Update dependencies
npm update

# Update major versions (carefully)
npm install package@latest

# Run tests
npm run test

# Rebuild and redeploy
npm run build
```

### Monitoring Checklist

- [ ] Check error logs daily
- [ ] Monitor performance metrics weekly
- [ ] Review security updates monthly
- [ ] Run dependency audits
- [ ] Backup configurations
- [ ] Test disaster recovery

## Cost Estimates

| Platform | Cost | Notes |
|----------|------|-------|
| Vercel Free | $0 | Up to 100K requests/month |
| Netlify Free | $0 | Up to 100GB/month |
| AWS S3 + CloudFront | $1-5/month | For high traffic |
| DigitalOcean | $5+/month | For dedicated server |
| Heroku | $7+/month | Simple deployment |

## Support & Resources

- [Vite Documentation](https://vitejs.dev)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [Vercel Deployment Guide](https://vercel.com/docs)
- [Netlify Deployment Guide](https://docs.netlify.com)

## Conclusion

The Autonomous Data Analyst Agent is designed for easy deployment across multiple platforms. Choose the platform that best fits your requirements for ease of use, cost, and scalability.

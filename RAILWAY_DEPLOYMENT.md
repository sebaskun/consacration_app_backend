# Railway Deployment Guide

This guide walks you through deploying the Totus Tuus backend to Railway.

## Prerequisites

1. [Railway account](https://railway.app)
2. Railway CLI installed: `npm install -g @railway/cli`
3. Git repository (recommended to push to GitHub/GitLab first)

## Step 1: Prepare Your Project

Ensure these files are in your backend directory:
- `Dockerfile` ✅
- `railway.json` ✅
- `requirements.txt` ✅
- `.env.railway` (template for environment variables) ✅

## Step 2: Create Railway Project

### Option A: Using Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo" and select your repository
4. Select the `backend_consagracion` folder as the root directory

### Option B: Using Railway CLI
```bash
# Login to Railway
railway login

# Initialize project in backend directory
cd backend_consagracion
railway init

# Link to a new project
railway link
```

## Step 3: Add PostgreSQL Database

1. In your Railway project dashboard, click "Add Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provision a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically set

## Step 4: Configure Environment Variables

In your Railway project dashboard, go to "Variables" and add:

```env
# Required - Generate a secure secret key
SECRET_KEY=your-very-long-and-secure-secret-key-for-production-at-least-32-characters

# JWT Configuration
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Totus Tuus - App de Consagración Total

# Environment
ENVIRONMENT=production

# Debug mode (set to false for production)
DEBUG_MODE=false

# CORS Origins - Update with your frontend domain
BACKEND_CORS_ORIGINS=https://your-frontend-domain.com,http://localhost:5173
```

**Important Notes:**
- `DATABASE_URL` is automatically provided by Railway's PostgreSQL service
- Generate a strong `SECRET_KEY` (you can use: `openssl rand -hex 32`)
- Update `BACKEND_CORS_ORIGINS` with your actual frontend domain

## Step 5: Deploy

### Option A: Automatic Deployment (Recommended)
If you connected via GitHub, Railway will automatically deploy on every push to the main branch.

### Option B: Manual Deployment via CLI
```bash
cd backend_consagracion
railway up
```

## Step 6: Run Database Migrations

After the first deployment, you need to run database migrations:

```bash
# Using Railway CLI
railway run alembic upgrade head

# Or connect to your service and run:
railway shell
alembic upgrade head
```

## Step 7: Verify Deployment

1. Check your Railway dashboard for the service URL
2. Visit `https://your-service-url.railway.app/docs` to see the API documentation
3. Test the health endpoint: `https://your-service-url.railway.app/health`

## Step 8: Update Frontend Configuration

Update your frontend's API base URL to point to your Railway deployment:

```typescript
// In frontend: src/services/api.ts
const API_BASE_URL = 'https://your-service-url.railway.app/api/v1'
```

## Troubleshooting

### Common Issues

1. **Build fails**: Check the build logs in Railway dashboard
2. **Database connection issues**: Ensure PostgreSQL service is running and `DATABASE_URL` is set
3. **CORS errors**: Update `BACKEND_CORS_ORIGINS` with your frontend domain
4. **Migration errors**: Run `railway run alembic upgrade head` manually

### Viewing Logs
```bash
# View recent logs
railway logs

# Follow logs in real-time
railway logs --follow
```

### Accessing the Database
```bash
# Connect to PostgreSQL
railway connect postgresql
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string (auto-provided) | `postgresql://user:pass@host:port/db` |
| `SECRET_KEY` | JWT secret key (min 32 chars) | `your-secure-secret-key-here` |
| `BACKEND_CORS_ORIGINS` | Allowed frontend origins | `https://mydomain.com,http://localhost:5173` |
| `ENVIRONMENT` | Application environment | `production` |
| `DEBUG_MODE` | Enable debug features | `false` |

## Production Checklist

- [ ] PostgreSQL database added and connected
- [ ] Strong `SECRET_KEY` generated and set
- [ ] `BACKEND_CORS_ORIGINS` updated with production domain
- [ ] `ENVIRONMENT` set to `production`
- [ ] `DEBUG_MODE` set to `false`
- [ ] Database migrations run successfully
- [ ] API endpoints working via HTTPS
- [ ] Frontend updated to use Railway API URL
- [ ] Health check endpoint responding

## Monitoring

Railway provides built-in monitoring:
- View metrics in the Railway dashboard
- Set up alerts for downtime
- Monitor resource usage and scaling

Your Totus Tuus backend is now deployed on Railway! 🚀
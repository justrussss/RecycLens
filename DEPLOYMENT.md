# Deployment Guide for RecycLens

## Option 1: Backend on Railway + Frontend on Netlify (Recommended)

### Step 1: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your RecycLens repository
5. Railway will auto-detect the Procfile and Python requirements
6. Set environment variables:
   - `FLASK_ENV=production`
7. Railway will assign you a URL (e.g., `https://your-app.up.railway.app`)
8. Note this URL for the next step

### Step 2: Deploy Frontend to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Sign in with GitHub
3. Click "Add new site" → "Import an existing project"
4. Select your RecycLens repository
5. Build settings:
   - Build command: `echo "Static site"` (or leave blank)
   - Publish directory: `static`
6. Create environment variable:
   - Key: `API_URL`
   - Value: `https://your-railway-backend.up.railway.app` (replace with your Railway URL)
7. Deploy

### Step 3: Update API Endpoint in Frontend

After you get your Railway backend URL:
1. Update `netlify.toml`:
   - Replace `https://your-railway-backend.up.railway.app` with your actual Railway URL
2. In `static/js/main.js`, the API calls will use the `API_URL` environment variable

## File Structure for Deployment

**Backend (Railway):**
- `app.py`
- `config.py`
- `models/`
- `requirements.txt`
- `Procfile`
- `static/` (can be included)
- `templates/` (can be included)

**Frontend (Netlify):**
- `static/` (CSS, JS, uploads folder)
- `netlify.toml`
- `package.json` (optional, for build hooks)

## Health Check

Both services should start automatically. Test:

```bash
# Backend health check
curl https://your-railway-backend.up.railway.app/health

# Frontend
https://your-netlify-site.netlify.app
```

## Troubleshooting

**CORS Errors:** Already configured in `app.py` with flask-cors

**500 Errors on Classification:** Check Railway logs for model/classifier issues

**404 on Images:** Ensure Netlify serves the `static` folder correctly

## Environment Variables

### Railway (Backend)
- `PORT` (auto-set by Railway)
- `FLASK_ENV=production`

### Netlify (Frontend)
- `API_URL=https://your-railway-backend.up.railway.app`

## Next Steps

1. Push all changes to GitHub
2. Follow the deployment steps above
3. Test the app at `https://your-netlify-site.netlify.app`
4. Upload an image and verify the backend processes it correctly

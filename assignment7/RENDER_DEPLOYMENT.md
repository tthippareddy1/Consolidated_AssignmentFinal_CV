# 🚀 Deploy Flask Backend to Render

## Quick Deployment Guide

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### Step 2: Create New Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Choose "Build and deploy from a Git repository"
4. Click "Next"

### Step 3: Connect Repository
1. Select your GitHub repository: `Consolidated_AssignmentFinal_CV`
2. Click "Connect"

### Step 4: Configure Service

Fill in these settings:

**Basic Settings:**
- **Name:** `cv-stereo-backend` (or any name)
- **Region:** Select closest to you
- **Branch:** `main`
- **Root Directory:** `assignment7`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:**
  ```
  pip install -r requirements_render.txt
  ```

- **Start Command:**
  ```
  gunicorn app:app
  ```

**Instance Type:**
- Select: **Free** (0.1 CPU, 512 MB RAM)

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Watch the logs for any errors

### Step 6: Get Your Backend URL

Once deployed, you'll get a URL like:
```
https://cv-stereo-backend.onrender.com
```

**Important:** Copy this URL - you'll need it!

### Step 7: Test Backend

Test the health endpoint:
```
https://YOUR-APP-NAME.onrender.com/api/health
```

Should return: `{"status": "ok", "calibrations": 0}`

---

## Update Frontend

After deployment, update `task1_stereo_measurement.html`:

**Find:**
```javascript
const API_URL = 'http://localhost:5001';
```

**Replace with:**
```javascript
const API_URL = 'https://YOUR-APP-NAME.onrender.com';
```

---

## ⚠️ Important Notes

### Free Tier Limitations:
- **Spins down after 15 minutes** of inactivity
- **First request takes 30-60 seconds** to wake up
- **512 MB RAM** (enough for this app)

### Add Loading Message:
Consider adding a note on your frontend:
```
"Backend may take 30-60 seconds to wake up on first use"
```

---

## 🐛 Troubleshooting

### Problem: Build fails with "opencv-python" error
**Solution:** Make sure you're using `requirements_render.txt` which has `opencv-python-headless`

### Problem: Application failed to respond
**Solution:** 
1. Check logs in Render dashboard
2. Verify start command is `gunicorn app:app`
3. Make sure `app.py` is in assignment7 folder

### Problem: CORS errors in browser
**Solution:** Backend already has CORS enabled, but verify the frontend is using HTTPS (not HTTP)

---

## 💰 Cost

**FREE!** Render's free tier includes:
- 750 hours/month (unlimited for one service)
- Automatic HTTPS
- Custom domains (optional)

---

## 🔄 To Update Backend Later

1. Push changes to GitHub
2. Render auto-deploys (if enabled)
3. Or manually click "Deploy latest commit"

---

## Alternative: Railway (If Render doesn't work)

1. Go to https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select `assignment7` folder
5. Add start command: `gunicorn app:app`
6. Add environment variable: `PORT=8080`

---

## 📧 Share with Professor

Once deployed, your professor can access:
- **Frontend:** `https://tthippareddy1.github.io/Consolidated_AssignmentFinal_CV/assignment7/task1_stereo_measurement.html`
- **Backend API:** `https://YOUR-APP.onrender.com`

Everything works online! ✅


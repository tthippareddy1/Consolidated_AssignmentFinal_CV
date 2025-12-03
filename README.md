# Computer Vision Modules Portfolio

Complete portfolio of 7 computer vision assignments with interactive web demonstrations.

## 📁 Project Structure

```
All Modules/
├── index.html              # Main landing page
├── styles.css              # Global styles
├── script.js               # Interactive features
├── assignment1/            # Perspective Measurement
├── assignment2/            # Template Matching
├── assignment3/            # Image Analysis Suite
├── assignment4/            # Image Stitching & Panorama
├── assignment5-6/          # SAM2 Segmentation & Tracking
└── assignment7/            # Stereo Vision & Pose Tracking
```

## ✅ What's Done

- ✅ Professional landing page created
- ✅ All 7 modules organized and linked
- ✅ Responsive design for mobile and desktop
- ✅ Evaluation section template (ready to fill)
- ✅ Modern UI with smooth animations

## 📝 Next Steps

### 1. Add Demo Videos

For each module, you need to:
- Record a demonstration video (2-5 minutes)
- Upload to YouTube, Google Drive, or similar
- Add the embed code or link to the landing page

**How to add videos:**
1. Find the video container for each module (search for `video-1`, `video-2`, etc. in `index.html`)
2. Replace the placeholder with:
   - YouTube embed: `<iframe width="560" height="315" src="YOUR_YOUTUBE_EMBED_URL"></iframe>`
   - Or a link: `<a href="YOUR_VIDEO_URL" target="_blank">Watch Demo Video</a>`

### 2. Complete Evaluation Study

Pick ONE feature from any module and test it on 10 different variations:

**Example metrics to use:**
- **Perspective Measurement**: Measurement accuracy (% error)
- **Template Matching**: Detection accuracy, precision, recall
- **Edge Detection**: Edge detection quality score
- **Panorama**: Alignment error, stitching quality
- **Stereo Vision**: Depth estimation error

**Steps:**
1. Choose your module/feature
2. Run 10 different test cases
3. Record results
4. Update the evaluation table in `index.html` (lines 233-295)
5. Add key findings in the summary section

### 3. Deploy to Public Hosting

Choose one of these options:

#### Option A: GitHub Pages (Recommended - FREE)
```bash
# 1. Create a new GitHub repository
# 2. Push your code
cd "/Users/tarunkumarreddythippareddy/Documents/computervision/All Modules"
git init
git add .
git commit -m "Initial commit - CV Portfolio"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main

# 3. Enable GitHub Pages in repository settings
# Settings > Pages > Source: main branch > Save
# Your site will be at: https://YOUR_USERNAME.github.io/REPO_NAME/
```

#### Option B: Netlify (Easy Drag & Drop - FREE)
1. Go to https://app.netlify.com/drop
2. Drag and drop your entire "All Modules" folder
3. Get instant public URL

#### Option C: Vercel (CLI Deploy - FREE)
```bash
npm install -g vercel
cd "/Users/tarunkumarreddythippareddy/Documents/computervision/All Modules"
vercel
```

### 4. Add Worksheets (if applicable)

If any assignment required theoretical work:
- Create PDF of your worksheets
- Upload to Google Drive or GitHub
- Add link to the landing page or submit directly to classroom

## 🧪 Testing Locally

Open the landing page in your browser:
```bash
cd "/Users/tarunkumarreddythippareddy/Documents/computervision/All Modules"
open index.html  # macOS
# or
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

## 📋 Submission Checklist

Before December 3, 11:59 PM Eastern:

- [ ] All 7 modules are functional and accessible
- [ ] Landing page deployed to public URL (not localhost)
- [ ] Demo video added for each module
- [ ] Evaluation study completed (10 variations)
- [ ] Results table filled in on landing page
- [ ] Public URL submitted to professor
- [ ] Any required worksheets uploaded as PDF

## 🎨 Customization Tips

### Change Colors
Edit `styles.css` variables (lines 9-18):
```css
:root {
    --primary-color: #2563eb;  /* Main blue color */
    --accent-color: #f59e0b;   /* Accent orange */
}
```

### Update Module Descriptions
Edit `index.html` module cards (lines 45-240)

### Add Your Name/Info
Edit header section in `index.html` (lines 10-13)

## 🚀 Quick Deploy Commands

```bash
# Navigate to project
cd "/Users/tarunkumarreddythippareddy/Documents/computervision/All Modules"

# Test locally
python3 -m http.server 8000

# Deploy to GitHub Pages (after setup)
git add .
git commit -m "Update portfolio"
git push
```

## 📞 Support

If modules aren't working:
1. Check browser console for errors (F12)
2. Ensure all file paths are correct
3. Test each module individually first
4. Verify all dependencies are loaded

---

**Deadline**: December 3, 2025 at 11:59 PM Eastern

**Important**: Submission portal closes after deadline - don't wait until last minute!


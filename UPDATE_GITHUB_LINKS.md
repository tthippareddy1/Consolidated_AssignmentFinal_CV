# 🔗 Update GitHub Repository Links

## After Creating Your GitHub Repository

Once you've created your GitHub repository and know its name, you need to update the placeholder links in `index.html`.

---

## Quick Update Method

### Option 1: Find & Replace (Easiest)

1. Open `index.html` in your code editor
2. Press `Cmd+F` (Mac) or `Ctrl+F` (Windows) to open Find & Replace
3. **Find:** `YOUR_REPO_NAME`
4. **Replace with:** Your actual repository name (e.g., `cv-portfolio`)
5. Click "Replace All"
6. Save the file

---

## Example

If your GitHub username is `tthippareddy1` and your repository is named `cv-portfolio`:

**Before:**
```html
https://github.com/tthippareddy1/YOUR_REPO_NAME/tree/main/assignment1
```

**After:**
```html
https://github.com/tthippareddy1/cv-portfolio/tree/main/assignment1
```

---

## Using Terminal (Advanced)

```bash
cd "/Users/tarunkumarreddythippareddy/Documents/computervision/All Modules"

# Replace YOUR_REPO_NAME with your actual repo name
sed -i '' 's/YOUR_REPO_NAME/cv-portfolio/g' index.html

# Commit the change
git add index.html
git commit -m "Update GitHub repository links"
git push
```

---

## What Gets Updated

All 7 assignments will have working GitHub links:

1. Assignment 1: `https://github.com/tthippareddy1/YOUR_REPO/tree/main/assignment1`
2. Assignment 2: `https://github.com/tthippareddy1/YOUR_REPO/tree/main/assignment2`
3. Assignment 3: `https://github.com/tthippareddy1/YOUR_REPO/tree/main/assignment3`
4. Assignment 4: `https://github.com/tthippareddy1/YOUR_REPO/tree/main/assignment4`
5. Assignment 5-6: `https://github.com/tthippareddy1/YOUR_REPO/tree/main/assignment5-6`
6. Assignment 7: `https://github.com/tthippareddy1/YOUR_REPO/tree/main/assignment7`

---

## Verify It Works

After updating and deploying:
1. Visit your live site
2. Click on any "📂 Source Code" button
3. It should take you to that assignment's folder on GitHub

---

## If You Change Repository Name Later

Just run the find & replace again with the new repository name!


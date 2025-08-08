# GitHub Pages Deployment Guide 🚀

This guide will help you deploy the Tao Income Tracker to GitHub Pages for free hosting.

## Prerequisites 📋

1. **GitHub Account**: You need a GitHub account
2. **Git**: Install Git on your computer
3. **Repository**: Create a new repository on GitHub

## Step-by-Step Deployment 📝

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon in the top right
3. Select "New repository"
4. Name it: `tao-income-tracker`
5. Make it **Public** (required for free GitHub Pages)
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### Step 2: Upload Your Code

**Option A: Using GitHub Desktop (Recommended for beginners)**
1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and sign in
3. Click "Clone a repository from the Internet"
4. Select your `tao-income-tracker` repository
5. Choose a local path
6. Click "Clone"
7. Copy all your project files to the cloned folder
8. In GitHub Desktop, you'll see all the changes
9. Add a commit message like "Initial commit"
10. Click "Commit to main"
11. Click "Push origin"

**Option B: Using Command Line**
```bash
# Navigate to your project folder
cd /path/to/your/tao-income-tracker

# Initialize git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit"

# Add your GitHub repository as remote
git remote add origin https://github.com/EZTrades-dev/tao-income-tracker.git

# Push to GitHub
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Scroll down to "Pages" section
4. Under "Source", select "Deploy from a branch"
5. Under "Branch", select "gh-pages" and "/(root)"
6. Click "Save"

### Step 4: Configure GitHub Actions

The `.github/workflows/deploy.yml` file will automatically:
- Deploy your site when you push changes
- Build and publish to the `gh-pages` branch
- Make your site available at `https://YOUR_USERNAME.github.io/tao-income-tracker`

### Step 5: Update Configuration Files

**Update package.json:**
Replace `yourusername` with your actual GitHub username in:
- `repository.url`
- `homepage`
- `bugs.url`

**Update CNAME (Optional):**
If you have a custom domain, replace the content with your domain.

### Step 6: Test Your Deployment

1. Wait 5-10 minutes for GitHub Actions to complete
2. Go to `https://YOUR_USERNAME.github.io/tao-income-tracker`
3. Your application should be live!

## Important Notes ⚠️

### CORS Limitations
Since this is a client-side application, users may encounter CORS errors when making API calls to tao.app. Solutions:

1. **Browser Extension**: Users can install "CORS Unblock" extension
2. **Local Development**: For full functionality, run locally with the backend
3. **Proxy Service**: Consider using a CORS proxy service

### API Key Security
- The API key is hardcoded in the frontend (not secure for production)
- For production use, consider:
  - Backend proxy server
  - Environment variables
  - User-specific API keys

### Rate Limiting
- The tao.app API has a 10 calls/minute limit
- Users should be aware of this limitation
- Consider implementing client-side rate limiting

## Custom Domain (Optional) 🌐

If you want to use a custom domain:

1. **Purchase a domain** (e.g., from Namecheap, GoDaddy)
2. **Add CNAME record** pointing to `YOUR_USERNAME.github.io`
3. **Update CNAME file** in your repository with your domain
4. **Wait for DNS propagation** (up to 24 hours)

## Troubleshooting 🔧

### Common Issues

**"Page not found" error:**
- Check that GitHub Pages is enabled
- Verify the branch is set to `gh-pages`
- Wait for deployment to complete

**CORS errors:**
- Users need to install CORS browser extension
- Or run the application locally with backend

**API calls failing:**
- Check that the API key is valid
- Verify the cold key address is correct
- Check network connectivity

### Getting Help

1. **Check GitHub Actions**: Go to Actions tab to see deployment logs
2. **GitHub Pages Settings**: Verify Pages is enabled and configured
3. **Repository Settings**: Check all settings are correct
4. **GitHub Support**: Use GitHub's help documentation

## Maintenance 🔄

### Updating Your Site

1. **Make changes** to your local files
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. **Wait for deployment** (usually 2-5 minutes)
4. **Check your site** for updates

### Monitoring

- **GitHub Actions**: Monitor deployment status
- **GitHub Pages**: Check site health
- **User Feedback**: Monitor issues and requests

## Security Considerations 🔒

### For Production Use

1. **API Key Management**: Don't hardcode API keys
2. **CORS Handling**: Implement proper CORS policies
3. **Rate Limiting**: Add client-side rate limiting
4. **Error Handling**: Improve error messages and logging
5. **Data Validation**: Add input validation

### Privacy

- **No Data Storage**: Application doesn't store user data
- **Client-Side Processing**: All calculations happen in browser
- **API Calls**: Only makes calls to tao.app API

---

**Your Tao Income Tracker will be live at: `https://EZTrades-dev.github.io/tao-income-tracker`** 🎉

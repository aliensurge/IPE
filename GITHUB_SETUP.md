# GitHub Setup Instructions

## Prerequisites
- Git installed on your system
- GitHub account created

## Step-by-Step Guide

### 1. Install Git (if not already installed)
- Download from: https://git-scm.com/download/win
- Or use winget: `winget install Git.Git`
- Restart your terminal after installation

### 2. Configure Git (First time only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Initialize Git Repository
```bash
git init
```

### 4. Add All Files
```bash
git add .
```

### 5. Create Initial Commit
```bash
git commit -m "Initial commit: Website Monitoring Dashboard"
```

### 6. Create GitHub Repository
- Go to https://github.com/new
- Create a new repository (don't initialize with README, .gitignore, or license)
- Copy the repository URL (e.g., `https://github.com/yourusername/website-monitoring-dashboard.git`)

### 7. Connect Local Repository to GitHub
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
```

### 8. Push to GitHub
```bash
git branch -M main
git push -u origin main
```

## Quick Reference Commands

### Daily Workflow
```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

### View Commit History
```bash
git log --oneline
```

### Update from GitHub
```bash
git pull
```



#!/bin/bash
# Render Deployment Script for Finansla Terminal V2

echo "🚀 Finansla Terminal V2 - Render Deployment Script"
echo "=================================================="
echo ""
echo "📋 This script helps you deploy to Render"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git found"
echo ""

# Check if repo is a git repository
if [ ! -d .git ]; then
    echo "⚠️  Not a git repository. Initializing..."
    git init
    git remote add origin https://github.com/EfehanTanir/finansla-terminal-v2.git
fi

echo "📤 Preparing for deployment..."
echo ""

# Make build script executable
chmod +x build.sh

echo "✅ Files prepared"
echo ""

# Add all files
git add .
echo "✅ Files staged for commit"

# Get commit message
read -p "Enter commit message (default: 'Deploy to Render'): " COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Deploy to Render"}

git commit -m "$COMMIT_MSG" || echo "ℹ️  Nothing new to commit"

echo ""
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🌐 Next steps:"
echo "1. Go to: https://dashboard.render.com"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Use these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: streamlit run main.py --server.port=10000 --server.address=0.0.0.0"
echo ""
echo "5. Add Environment Variables:"
echo "   - FINNHUB_API_KEY=your_key"
echo "   - ALPHA_VANTAGE_API_KEY=your_key"
echo "   - DEFAULT_DATA_PROVIDER=yfinance"
echo ""
echo "6. Click 'Create Web Service' and wait for deployment!"
echo ""
echo "📖 Full guide: See RENDER_DEPLOY.md"
echo ""
echo "💡 Tip: Your app will be live at: https://finansla-terminal-v2.onrender.com"

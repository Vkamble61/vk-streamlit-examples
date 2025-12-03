#!/bin/bash

# Quick Deployment Script for Streamlit App
# Run this script to prepare and commit deployment files

echo "🚀 Preparing app for deployment..."

# Navigate to project directory
cd /workspaces/vk-streamlit-examples

# Check git status
echo "📋 Current changes:"
git status --short

# Add files (excluding secrets)
echo ""
echo "➕ Adding files to git..."
git add websites-and-documents-chatbot/.streamlit/config.toml
git add websites-and-documents-chatbot/.gitignore
git add websites-and-documents-chatbot/DEPLOYMENT.md
git add websites-and-documents-chatbot/src/web_and_docs_chatbot/streamlit_bot.py

# Show what will be committed
echo ""
echo "📝 Files to be committed:"
git status --short

echo ""
echo "✅ Files are staged and ready to commit!"
echo ""
echo "Next steps:"
echo "1. Commit: git commit -m 'Add deployment configuration'"
echo "2. Push: git push origin main"
echo "3. Deploy: Visit https://share.streamlit.io"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions"

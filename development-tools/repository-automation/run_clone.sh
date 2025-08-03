#!/bin/bash

echo "🚀 GitHub Repository Consolidation Script"
echo "=========================================="
echo ""
echo "This script will clone all public repositories from:"
echo "- murilobiss@gmail.com (GitHub: murilobiss)"
echo "- mbxagency@gmail.com (GitHub: mbxagency)"
echo ""
echo "All repositories will be independent copies (not forks)"
echo "Target directory: ~/Desktop/GitDataEng/"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Run the cloning script
echo ""
echo "🔍 Starting repository cloning process..."
python3 clone_repositories.py

echo ""
echo "✅ Process completed!"
echo "Check the GitDataEng/ folder for your consolidated repositories." 
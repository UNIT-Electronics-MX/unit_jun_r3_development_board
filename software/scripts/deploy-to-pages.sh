#!/bin/bash
# Build documentation for GitHub Actions deployment
# This script builds documentation in software/book/book/ for GitHub Actions to deploy

echo "🚀 Building documentation for GitHub Actions..."

# Build documentation (does NOT modify docs/ directory)
echo "📖 Building documentation..."
python3 software/scripts/build_docs.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

# Check if book directory was created
if [ ! -d "software/book/book" ]; then
    echo "❌ software/book/book/ directory not found after build!"
    exit 1
fi

echo "📊 Files in software/book/book/ directory:"
ls -la software/book/book/

echo "✅ Documentation built successfully!"
echo "🚀 GitHub Actions will deploy from software/book/book/ directory"
echo "ℹ️  docs/ directory remains untouched for existing Pages setup"

# Add software/book/book to git if requested
read -p "Do you want to commit the built documentation? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📁 Adding software/book/book/ to git..."
    git add software/book/book/
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        echo "ℹ️  No changes to commit in software/book/book/"
    else
        # Commit changes
        echo "💾 Committing documentation changes..."
        git commit -m "📚 Update mdBook documentation build

        - Generated from README files
        - Updated: $(date)
        - Branch: $(git branch --show-current)
        - Commit: $(git rev-parse --short HEAD)"
        
        # Push to repository
        echo "🚀 Pushing to repository..."
        git push origin $(git branch --show-current)
        
        if [ $? -eq 0 ]; then
            echo "✅ Documentation successfully pushed!"
            echo "🌐 GitHub Actions will deploy automatically"
        else
            echo "❌ Failed to push to repository!"
            exit 1
        fi
    fi
else
    echo "ℹ️  Documentation built but not committed"
fi

echo "🎉 Build process completed!"

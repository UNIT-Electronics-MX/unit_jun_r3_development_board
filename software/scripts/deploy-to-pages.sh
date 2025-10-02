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

# Add simple navbar links to all HTML files
echo "🔗 Adding clean navbar links..."
for html_file in software/book/book/*.html software/book/book/*/*.html software/book/book/*/*/*.html; do
    if [ -f "$html_file" ]; then
        # Insert minimal navbar links before closing body tag
        sed -i '/<\/body>/i\
<script>\
document.addEventListener("DOMContentLoaded", function() {\
    setTimeout(function() {\
        const menuBar = document.querySelector(".menu-bar .right-buttons");\
        if (menuBar) {\
            const shopLink = document.createElement("a");\
            shopLink.href = "https://uelectronics.com/";\
            shopLink.target = "_blank";\
            shopLink.innerHTML = "🛒";\
            shopLink.title = "Shop";\
            shopLink.style.cssText = "color: #666; text-decoration: none; padding: 4px; font-size: 14px; margin-right: 4px; border: 1px solid #ddd; border-radius: 3px; transition: all 0.2s ease; display: inline-block; text-align: center; width: 24px; height: 24px; line-height: 16px;";\
            shopLink.onmouseover = function() { this.style.borderColor = "#999"; this.style.backgroundColor = "#f5f5f5"; };\
            shopLink.onmouseout = function() { this.style.borderColor = "#ddd"; this.style.backgroundColor = "transparent"; };\
            \
            const repoLink = document.createElement("a");\
            repoLink.href = "https://github.com/UNIT-Electronics-MX/unit_jun_r3_development_board";\
            repoLink.target = "_blank";\
            repoLink.innerHTML = "📋";\
            repoLink.title = "Repository";\
            repoLink.style.cssText = "color: #666; text-decoration: none; padding: 4px; font-size: 14px; margin-right: 4px; border: 1px solid #ddd; border-radius: 3px; transition: all 0.2s ease; display: inline-block; text-align: center; width: 24px; height: 24px; line-height: 16px;";\
            repoLink.onmouseover = function() { this.style.borderColor = "#999"; this.style.backgroundColor = "#f5f5f5"; };\
            repoLink.onmouseout = function() { this.style.borderColor = "#ddd"; this.style.backgroundColor = "transparent"; };\
            \
            menuBar.insertBefore(repoLink, menuBar.firstChild);\
            menuBar.insertBefore(shopLink, menuBar.firstChild);\
        }\
    }, 100);\
});\
</script>' "$html_file"
    fi
done

echo "✅ Documentation built successfully!"

# Copy to docs/ directory for GitHub Pages deployment
echo "📂 Copying documentation to docs/ directory..."

# Remove existing content from docs/ (except PDFs if any)
find docs -name "*.html" -delete 2>/dev/null || true
find docs -name "*.css" -delete 2>/dev/null || true
find docs -name "*.js" -delete 2>/dev/null || true
find docs -type d -name "FontAwesome" -exec rm -rf {} + 2>/dev/null || true
find docs -type d -name "fonts" -exec rm -rf {} + 2>/dev/null || true
find docs -type d -name "css" -exec rm -rf {} + 2>/dev/null || true
find docs -type d -name "resources" -exec rm -rf {} + 2>/dev/null || true
find docs -type d -name "hardware" -exec rm -rf {} + 2>/dev/null || true
find docs -type d -name "software" -exec rm -rf {} + 2>/dev/null || true

# Copy new built content to docs/
cp -r software/book/book/* docs/

echo "📊 Updated docs/ directory contents:"
ls -la docs/ | head -10

# Force commit the updated docs/ directory
echo "💾 Committing updated documentation to docs/..."
git add docs/

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes detected in docs/ directory"
else
    # Force commit changes
    echo "� Committing documentation updates..."
    git commit -m "� Auto-update documentation in docs/

    - Built from latest README content  
    - Generated: $(date)
    - Updated navbar with Shop and Repository icons
    - Commit: $(git rev-parse --short HEAD)"
    
    # Push to repository to trigger deployment
    echo "� Pushing to trigger GitHub Pages deployment..."
    git push origin $(git branch --show-current)
    
    if [ $? -eq 0 ]; then
        echo "✅ Documentation successfully updated and pushed!"
        echo "🌐 GitHub Pages will deploy automatically in a few minutes"
        echo "📋 Check deployment status at: https://github.com/UNIT-Electronics-MX/unit_jun_r3_development_board/actions"
    else
        echo "❌ Failed to push to repository!"
        exit 1
    fi
fi

echo "🎉 Documentation deployment process completed!"

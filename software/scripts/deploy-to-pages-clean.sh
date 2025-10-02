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
        # Insert simple navbar links before closing body tag
        sed -i '/<\/body>/i\
<script>\
document.addEventListener("DOMContentLoaded", function() {\
    setTimeout(function() {\
        const menuBar = document.querySelector(".menu-bar .left-buttons");\
        if (menuBar) {\
            const shopLink = document.createElement("a");\
            shopLink.href = "https://uelectronics.com/";\
            shopLink.target = "_blank";\
            shopLink.innerHTML = "Shop";\
            shopLink.style.cssText = "background-color: #ff6b35; color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-size: 12px; margin-left: 8px; transition: all 0.2s ease;";\
            shopLink.onmouseover = function() { this.style.backgroundColor = "#e55a2b"; this.style.transform = "translateY(-1px)"; };\
            shopLink.onmouseout = function() { this.style.backgroundColor = "#ff6b35"; this.style.transform = "translateY(0)"; };\
            \
            const repoLink = document.createElement("a");\
            repoLink.href = "https://github.com/UNIT-Electronics-MX/unit_jun_r3_development_board";\
            repoLink.target = "_blank";\
            repoLink.innerHTML = "Repository";\
            repoLink.style.cssText = "background-color: #24292e; color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-size: 12px; margin-left: 8px; transition: all 0.2s ease;";\
            repoLink.onmouseover = function() { this.style.backgroundColor = "#1a1e22"; this.style.transform = "translateY(-1px)"; };\
            repoLink.onmouseout = function() { this.style.backgroundColor = "#24292e"; this.style.transform = "translateY(0)"; };\
            \
            menuBar.appendChild(shopLink);\
            menuBar.appendChild(repoLink);\
        }\
    }, 100);\
});\
</script>' "$html_file"
    fi
done

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

#!/bin/bash

# Setup script for mdBook documentation development
# This script installs mdBook and sets up the development environment

set -e  # Exit on any error

echo "🚀 Setting up mdBook development environment..."

# Check if we're on macOS, Linux, or Windows
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "📋 Detected OS: $MACHINE"

# Function to install mdBook on different platforms
install_mdbook() {
    echo "📚 Installing mdBook..."
    
    case $MACHINE in
        Linux|Cygwin|MinGw)
            # Try to install via cargo if available
            if command -v cargo &> /dev/null; then
                echo "   Installing via Cargo..."
                cargo install mdbook
            else
                # Download binary release
                echo "   Downloading binary release..."
                LATEST_VERSION=$(curl -s https://api.github.com/repos/rust-lang/mdBook/releases/latest | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')
                DOWNLOAD_URL="https://github.com/rust-lang/mdBook/releases/download/${LATEST_VERSION}/mdbook-${LATEST_VERSION}-x86_64-unknown-linux-gnu.tar.gz"
                
                curl -sSL $DOWNLOAD_URL | tar -xz
                sudo mv mdbook /usr/local/bin/
                rm -f mdbook
            fi
            ;;
        Mac)
            # Try Homebrew first, then cargo
            if command -v brew &> /dev/null; then
                echo "   Installing via Homebrew..."
                brew install mdbook
            elif command -v cargo &> /dev/null; then
                echo "   Installing via Cargo..."
                cargo install mdbook
            else
                echo "❌ Please install either Homebrew or Rust/Cargo first"
                exit 1
            fi
            ;;
        *)
            echo "❌ Unsupported operating system: $MACHINE"
            echo "   Please install mdBook manually from: https://rust-lang.github.io/mdBook/guide/installation.html"
            exit 1
            ;;
    esac
}

# Check if mdBook is already installed
if command -v mdbook &> /dev/null; then
    MDBOOK_VERSION=$(mdbook --version)
    echo "✅ mdBook is already installed: $MDBOOK_VERSION"
else
    install_mdbook
fi

# Verify installation
if command -v mdbook &> /dev/null; then
    MDBOOK_VERSION=$(mdbook --version)
    echo "✅ mdBook installed successfully: $MDBOOK_VERSION"
else
    echo "❌ mdBook installation failed"
    exit 1
fi

# Navigate to book directory and test build
echo "🔨 Testing documentation build..."
cd software/book

# Build the documentation
if mdbook build; then
    echo "✅ Documentation build successful!"
    echo "📁 Output generated in: software/book/book/"
else
    echo "❌ Documentation build failed"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📚 To work with the documentation:"
echo "   cd software/book"
echo "   mdbook serve --open    # Start development server"
echo "   mdbook build          # Build static HTML"
echo "   mdbook clean          # Clean build artifacts"
echo ""
echo "🌐 Development server will be available at: http://localhost:3000"

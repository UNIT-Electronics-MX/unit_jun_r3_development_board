#!/bin/bash
# Quick deployment script for UNIT Touch Capacitive Sensor Documentation

echo "🚀 Starting quick documentation deployment..."

# Build documentation
echo "📖 Building documentation..."
python3 software/scripts/build_docs.py

# Serve locally for testing
echo "🌐 Serving documentation locally..."
echo "📱 Open http://localhost:3000 in your browser"
echo "Press Ctrl+C to stop"

cd software/book
mdbook serve --port 3000

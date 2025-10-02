# GitHub Scripts

This directory contains all automation scripts for the documentation build and deployment process.

## Structure

```
.github/scripts/
├── config.sh              # Configuration parameters (no hardcoded values)
├── navbar-builder.sh       # Navbar builder functions
├── deploy-to-pages.sh      # Main deployment script
├── build_docs.py          # Python documentation builder
└── smart-extract-docs.py  # README content extraction
```

## Scripts

### config.sh
Contains all configurable parameters including:
- Navigation URLs (Shop, Repository)
- Icons and styling
- Build directories
- Git configuration

### navbar-builder.sh
Modular functions for building navbar elements into HTML files:
- `generate_navbar_js()` - Creates JavaScript navbar code
- `build_navbar_into_files()` - Builds navbar into HTML files

### deploy-to-pages.sh
Main deployment script that:
1. Builds documentation using Python scripts
2. Injects configurable navbar
3. Copies to docs/ directory
4. Commits and pushes changes

### build_docs.py
Python script that:
- Calls smart-extract-docs.py
- Builds mdBook documentation
- Handles all content processing

### smart-extract-docs.py
Intelligent content extraction from README files:
- Processes multiple README files
- Handles image path corrections
- Copies resources and PDFs
- Generates clean mdBook structure

## Usage

### Local Development
```bash
# From repository root
./.github/scripts/deploy-to-pages.sh
```

### GitHub Actions
The workflow automatically uses these scripts for CI/CD deployment.

## Configuration

Edit `.github/scripts/config.sh` to modify:
- Shop URL
- Repository URL
- Icons and styling
- Build parameters

No hardcoded values in the main scripts - everything is configurable!

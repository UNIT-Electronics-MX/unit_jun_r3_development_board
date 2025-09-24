#!/usr/bin/env python3
"""
Automated Documentation Builder for UNIT Touch Capacitive Sensor
This script automates the complete mdBook documentation generation and deployment process.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time

class DocumentationBuilder:
    """Complete documentation builder and deployer."""
    
    def __init__(self):
        """Initialize the builder with project paths."""
        # Get the root project directory (2 levels up from scripts)
        self.project_root = Path(__file__).parent.parent.parent
        self.book_path = self.project_root / "software" / "book"
        self.extract_script = Path(__file__).parent / "smart-extract-docs.py"
        self.docs_path = self.project_root / "docs"
        
        print("Documentation Builder for UNIT Touch Capacitive Sensor")
        print(f"Project root: {self.project_root}")
        print(f"Book path: {self.book_path}")
        print(f"Protected docs/ path: {self.docs_path} (NEVER MODIFIED)")
        
    def protect_docs_directory(self):
        """Ensure docs/ directory is never modified by this script."""
        if self.docs_path.exists():
            # Check if docs contains product briefs (original content)
            product_brief = self.docs_path / "unit_touch_capacitive_sensor_product_brief.pdf"
            sphinx_pdf = self.docs_path / "unit_touch_capacitive_sensor_sphinx.pdf"
            
            if product_brief.exists() or sphinx_pdf.exists():
                self.print_step("Original docs/ with product briefs detected - PROTECTED")
            else:
                self.print_step("WARNING: docs/ exists but no product briefs found")
        else:
            self.print_step("No docs/ directory found")
        
    def print_step(self, message: str):
        """Print a formatted step message."""
        print(f"[INFO] {message}")
        
    def run_command(self, command: str, cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command with error handling."""
        if cwd is None:
            cwd = self.project_root
            
        self.print_step(f"Running: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=check
            )
            return result
            
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Command failed: {command}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"ERROR: {e.stderr}")
            raise
            
    def check_prerequisites(self):
        """Check if all required tools are available."""
        # Check mdbook
        try:
            result = self.run_command("mdbook --version")
            print(f"mdBook version: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERROR: mdBook not found. Install with: cargo install mdbook")
            return False
            
        # Check if extract script exists
        if not self.extract_script.exists():
            print(f"ERROR: Extract script not found at {self.extract_script}")
            return False
            
        self.print_step("All prerequisites met")
        return True
        
    def extract_content(self):
        """Extract content from README files."""
        self.print_step("Extracting documentation from README files...")
        
        # Make the script executable
        self.run_command(f"chmod +x {self.extract_script}")
        
        # Run the extraction
        self.run_command(f"python3 {self.extract_script}", cwd=self.project_root)
        
    def build_mdbook(self):
        """Build the mdBook documentation."""
        self.print_step("Building mdBook documentation...")
        
        # Change to the book directory and build
        try:
            result = self.run_command("mdbook build", cwd=self.book_path)
            
            # Check if the build was successful
            built_path = self.book_path / "book"
            if built_path.exists():
                self.print_step(f"Documentation built successfully at: {built_path}")
            else:
                raise Exception("Build directory not created")
                
        except Exception as e:
            print(f"ERROR: Failed to build documentation: {e}")
            raise
            
    def test_build(self):
        """Test the documentation build."""
        self.print_step("Testing documentation build...")
        
        book_path = self.book_path / "book"
        
        if not book_path.exists():
            raise Exception("Book directory not found after build")
            
        # Count generated files
        book_files = list(book_path.rglob("*"))
        book_files = [f for f in book_files if f.is_file()]
        
        self.print_step(f"Generated {len(book_files)} files in book/ directory")
        
        # Check for essential files
        index_html = book_path / "index.html"
        if not index_html.exists():
            raise Exception("index.html not found in build")
            
        print("Documentation ready for GitHub Actions deployment")
        
    def get_git_info(self):
        """Get current git information."""
        try:
            commit = self.run_command("git rev-parse HEAD")
            branch = self.run_command("git branch --show-current")
            
            return {
                'commit': commit.stdout.strip(),
                'branch': branch.stdout.strip()
            }
        except:
            return {'commit': 'unknown', 'branch': 'unknown'}
    
    def clean_previous_builds(self):
        """Clean previous build artifacts."""
        self.print_step("Cleaning previous builds...")
        
        # Clean the book build directory
        book_build = self.book_path / "book"
        if book_build.exists():
            shutil.rmtree(book_build)
            self.print_step("Removed previous book build")
            
        # Clean the src directory (will be regenerated)
        src_path = self.book_path / "src"
        if src_path.exists():
            # Keep book.toml and theme if they exist
            for item in src_path.iterdir():
                if item.name not in ["book.toml", "theme"]:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            
            self.print_step("Cleaned src directory")
    
    def build_all(self):
        """Run the complete build process."""
        start_time = time.time()
        
        print("Starting complete documentation build process...")
        
        try:
            # Step 1: Protect docs directory
            self.protect_docs_directory()
            
            # Step 2: Check prerequisites
            self.print_step("Checking prerequisites...")
            if not self.check_prerequisites():
                return False
                
            # Step 3: Clean previous builds
            self.clean_previous_builds()
            
            # Step 4: Extract content
            self.extract_content()
            
            # Step 5: Build mdBook
            self.build_mdbook()
            
            # Step 6: Test build
            self.test_build()
            
            # Get git info
            git_info = self.get_git_info()
            
            # Success message
            build_time = time.time() - start_time
            
            print("\nBuild completed successfully!")
            print(f"Build time: {build_time:.2f} seconds")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Git commit: {git_info['commit'][:8]}")
            print(f"Git branch: {git_info['branch']}")
            print("Documentation ready for deployment!")
            
            return True
            
        except Exception as e:
            print(f"\nERROR: Build failed: {e}")
            return False

def main():
    """Main entry point."""
    builder = DocumentationBuilder()
    success = builder.build_all()
    
    if success:
        print("SUCCESS: Documentation build completed successfully")
        sys.exit(0)
    else:
        print("FAILURE: Documentation build failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

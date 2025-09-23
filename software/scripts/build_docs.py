#!/usr/bin/env python3
"""
Automated Documentation Builder for UNIT JUN R3 Development Board
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
        self.extract_script = Path(__file__).parent / "smart-extract-docs.py"  # Now in same directory
        self.docs_path = self.project_root / "docs"  # PROTECTED DIRECTORY
        
        print(f"🏗️  Documentation Builder for UNIT JUN R3 Development Board")
        print(f"📁 Project root: {self.project_root}")
        print(f"📚 Book path: {self.book_path}")
        print(f"🚨 Protected docs/ path: {self.docs_path} (NEVER MODIFIED)")
        
    def protect_docs_directory(self):
        """Ensure docs/ directory is never modified by this script."""
        if self.docs_path.exists():
            # Check if docs contains product briefs (original content)
            product_brief = self.docs_path / "unit_touch_capacitive_sensor_product_brief.pdf"
            sphinx_pdf = self.docs_path / "unit_touch_capacitive_sensor_sphinx.pdf"
            
            if product_brief.exists() or sphinx_pdf.exists():
                self.print_step("✅ Original docs/ with product briefs detected - PROTECTED", "🛡️")
            else:
                self.print_step("⚠️  docs/ exists but no product briefs found", "⚠️")
        else:
            self.print_step("ℹ️  No docs/ directory found", "ℹ️")
        
    def print_step(self, message: str, emoji: str = "📝"):
        """Print a formatted step message."""
        print(f"{emoji} {message}")
        
    def run_command(self, command: str, cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command with error handling."""
        if cwd is None:
            cwd = self.project_root
            
        self.print_step(f"Running: {command}", "⚡")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=check
            )
            
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                print(f"⚠️  Error: {result.stderr}")
                
            return result
            
        except subprocess.CalledProcessError as e:
            self.print_step(f"Command failed: {e}", "❌")
            if e.stdout:
                print(f"stdout: {e.stdout}")
            if e.stderr:
                print(f"stderr: {e.stderr}")
            if check:
                sys.exit(1)
            return e
            
    def check_prerequisites(self) -> bool:
        """Check if all required tools are installed."""
        self.print_step("Checking prerequisites...", "🔍")
        
        # Check if mdbook is installed
        try:
            result = self.run_command("mdbook --version", check=False)
            if result.returncode != 0:
                self.print_step("mdbook not found. Please install it:", "❌")
                print("  curl -L https://github.com/rust-lang/mdBook/releases/download/v0.4.52/mdbook-v0.4.52-x86_64-unknown-linux-gnu.tar.gz | tar xz")
                print("  sudo mv mdbook /usr/local/bin/")
                return False
        except Exception:
            self.print_step("mdbook not found", "❌")
            return False
            
        # Check if extraction script exists
        if not self.extract_script.exists():
            self.print_step(f"Extraction script not found: {self.extract_script}", "❌")
            return False
            
        self.print_step("All prerequisites met", "✅")
        return True
        
    def extract_documentation(self):
        """Run the documentation extraction script."""
        self.print_step("Extracting documentation from README files...", "📖")
        
        # Make sure the script is executable
        self.run_command(f"chmod +x {self.extract_script}")
        
        # Run the extraction script
        self.run_command(f"python3 {self.extract_script}")
        
    def build_mdbook(self):
        """Build the mdBook documentation."""
        self.print_step("Building mdBook documentation...", "🔨")
        
        # Ensure we're in the book directory
        if not self.book_path.exists():
            self.print_step(f"Book directory not found: {self.book_path}", "❌")
            sys.exit(1)
            
        # Build the book
        self.run_command("mdbook build", cwd=self.book_path)
        
        built_path = self.book_path / "book"
        if built_path.exists():
            self.print_step(f"Documentation built successfully at: {built_path}", "✅")
        else:
            self.print_step("Build failed - no output directory found", "❌")
            sys.exit(1)
            
    def test_build(self):
        """Test the built documentation locally."""
        self.print_step("Testing documentation build...", "🧪")
        
        # Check if index.html exists in book directory
        book_index = self.book_path / "book" / "index.html"
        
        if not book_index.exists():
            self.print_step("index.html not found in book build output", "❌")
            sys.exit(1)
            
        # Count generated files
        book_files = list((self.book_path / "book").rglob("*"))        
        self.print_step(f"Generated {len(book_files)} files in book/ directory", "📊")
        self.print_step("Documentation ready for GitHub Actions deployment", "�")
        
    def serve_locally(self, port: int = 3000):
        """Serve the documentation locally for testing."""
        self.print_step(f"Starting local server on port {port}...", "🌐")
        print(f"📱 Open in browser: http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        try:
            self.run_command(f"mdbook serve --port {port}", cwd=self.book_path)
        except KeyboardInterrupt:
            self.print_step("Server stopped", "⏹️")
            
    def clean_build(self):
        """Clean previous build artifacts."""
        self.print_step("Cleaning previous builds...", "🧹")
        
        # Remove book output directory
        book_output = self.book_path / "book"
        if book_output.exists():
            shutil.rmtree(book_output)
            self.print_step("Removed previous book build", "🗑️")
            
        # Clean src directory (will be regenerated)
        src_dir = self.book_path / "src"
        if src_dir.exists():
            # Keep only book.toml and theme directory
            for item in src_dir.iterdir():
                if item.name not in ["book.toml", "theme"]:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            self.print_step("Cleaned src directory", "🧽")
            
    def get_build_info(self) -> dict:
        """Get information about the current build."""
        info = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project_root": str(self.project_root),
            "book_path": str(self.book_path),
        }
        
        # Get git information if available
        try:
            result = self.run_command("git rev-parse HEAD", check=False)
            if result.returncode == 0:
                info["git_commit"] = result.stdout.strip()
                
            result = self.run_command("git branch --show-current", check=False)
            if result.returncode == 0:
                info["git_branch"] = result.stdout.strip()
        except:
            pass
            
        return info
        
    def build_complete(self):
        """Complete build process with all steps."""
        start_time = time.time()
        
        self.print_step("Starting complete documentation build process...", "🚀")
        
        # Protect docs directory first
        self.protect_docs_directory()
        
        # Check prerequisites
        if not self.check_prerequisites():
            sys.exit(1)
            
        # Clean previous builds
        self.clean_build()
        
        # Extract documentation
        self.extract_documentation()
        
        # Build mdBook
        self.build_mdbook()
        
        # Test build
        self.test_build()
        
        # Show build info
        build_info = self.get_build_info()
        elapsed = time.time() - start_time
        
        self.print_step("Build completed successfully!", "🎉")
        self.print_step(f"Build time: {elapsed:.2f} seconds", "⏱️")
        self.print_step(f"Timestamp: {build_info['timestamp']}", "📅")
        
        if "git_commit" in build_info:
            self.print_step(f"Git commit: {build_info['git_commit'][:8]}", "🔗")
        if "git_branch" in build_info:
            self.print_step(f"Git branch: {build_info['git_branch']}", "🌿")
            
        self.print_step("Documentation ready for deployment!", "📚")

def main():
    """Main entry point with command line argument handling."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build UNIT JUN R3 Development Board Documentation")
    parser.add_argument("--serve", "-s", action="store_true", help="Serve documentation locally after building")
    parser.add_argument("--port", "-p", type=int, default=3000, help="Port for local server (default: 3000)")
    parser.add_argument("--clean-only", "-c", action="store_true", help="Only clean build artifacts")
    parser.add_argument("--extract-only", "-e", action="store_true", help="Only extract documentation")
    parser.add_argument("--build-only", "-b", action="store_true", help="Only build mdBook (skip extraction)")
    
    args = parser.parse_args()
    
    builder = DocumentationBuilder()
    
    try:
        if args.clean_only:
            builder.clean_build()
        elif args.extract_only:
            if builder.check_prerequisites():
                builder.extract_documentation()
        elif args.build_only:
            if builder.check_prerequisites():
                builder.build_mdbook()
                builder.test_build()
        else:
            # Complete build process
            builder.build_complete()
            
            if args.serve:
                builder.serve_locally(args.port)
                
    except KeyboardInterrupt:
        builder.print_step("Build interrupted by user", "⏹️")
        sys.exit(1)
    except Exception as e:
        builder.print_step(f"Unexpected error: {e}", "💥")
        sys.exit(1)

if __name__ == "__main__":
    main()

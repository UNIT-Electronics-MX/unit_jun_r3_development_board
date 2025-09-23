#!/usr/bin/env python3
"""
Extractor inteligente de contenido que NO duplica títulos
Extrae SOLO el contenido útil sin alterar los README originales
"""

import os
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any

def print_status(message: str, emoji: str = "📝"):
    """Print a formatted status message."""
    print(f"{emoji} {message}")

def fix_image_sizes(content: str) -> str:
    """Fix image sizes for better display in mdBook, preserving HTML link structure."""
    
    # First, handle HTML link structures with images - these should be preserved as-is but with better styling
    # Pattern: <a href="..."><img src="..." width="..." ...><br/> Text</a>
    content = re.sub(
        r'<a href="([^"]+)"><img src="([^"]+)"[^>]*><br/>\s*([^<]*)</a>',
        r'<div align="center"><a href="\1"><img src="\2" style="max-width: 500px; height: auto;" alt="\3"><br/> \3</a></div>',
        content
    )
    
    # Handle standalone img tags with width attribute (not part of links)
    # We'll temporarily mark linked images to avoid processing them
    temp_placeholder = "___LINKED_IMG___"
    
    # Temporarily replace linked images
    linked_images = []
    def store_linked_img(match):
        linked_images.append(match.group(0))
        return f"{temp_placeholder}{len(linked_images)-1}___"
    
    content = re.sub(r'<a[^>]*>.*?<img[^>]*>.*?</a>', store_linked_img, content, flags=re.DOTALL)
    
    # Now process standalone images
    content = re.sub(
        r'<img src="([^"]+)" width="[^"]*"([^>]*)>',
        r'<img src="\1" style="max-width: 80%; height: auto;"\2>',
        content
    )
    
    # Fix other standalone HTML img tags
    content = re.sub(
        r'<img src="([^"]+)" alt="([^"]*)"[^>]*>',
        r'<div align="center"><img src="\1" alt="\2" style="max-width: 80%; height: auto;"></div>',
        content
    )
    
    # Fix markdown images by adding HTML wrapper for sizing
    content = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        r'<div align="center"><img src="\2" alt="\1" style="max-width: 70%; height: auto;"></div>',
        content
    )
    
    # Restore linked images
    for i, linked_img in enumerate(linked_images):
        content = content.replace(f"{temp_placeholder}{i}___", linked_img)
    
    return content

def preserve_external_links(content: str) -> str:
    """Preserve HTML and PDF links as-is, fix local resource paths."""
    
    # Fix local image src references to use resources folder
    content = re.sub(
        r'src="\./resources/([^"]+)"',
        r'src="../resources/\1"',
        content
    )
    
    content = re.sub(
        r'src="resources/([^"]+)"',
        r'src="../resources/\1"',
        content
    )
    
    # Fix href links to local resources
    content = re.sub(
        r'href="\./resources/([^"]+)"',
        r'href="../resources/\1"',
        content
    )
    
    # Fix href links to PDF files in root hardware directory
    content = re.sub(
        r'href="\./([^"]+\.pdf)"',
        r'href="../resources/\1"',
        content
    )
    
    # Fix markdown image references
    content = re.sub(
        r'!\[([^\]]*)\]\(\./resources/([^)]+)\)',
        r'![\1](../resources/\2)',
        content
    )
    
    return content

def extract_content_without_main_title(content: str, page_title: str) -> str:
    """Extract content removing the main title to avoid duplication."""
    
    # Clean YAML frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL | re.MULTILINE)
    
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove template instructions
    template_phrases = [
        r'This file serves as an input.*?(?=\n#|\n\n|$)',
        r'Fill in each section.*?(?=\n#|\n\n|$)',
        r'FILL HERE.*?(?=\n|\s)',
        r'========================================.*?========================================',
        r'Edita los valores.*?(?=\n|\s)',
        r'El formato se mantendrá.*?(?=\n|\s)'
    ]
    
    for phrase in template_phrases:
        content = re.sub(phrase, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Split into lines and process
    lines = content.split('\n')
    result_lines = []
    skip_first_title = True
    
    for line in lines:
        # Skip the first main title (# Title) to avoid duplication
        if skip_first_title and line.strip().startswith('# '):
            skip_first_title = False
            continue
        
        # Add all other content
        result_lines.append(line)
    
    # Clean up multiple empty lines
    result = '\n'.join(result_lines)
    result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
    
    # Fix image paths
    result = re.sub(r'hardware/resources/', './resources/', result)
    result = re.sub(r'\.\./\.\./\.\./\.\./hardware/resources/', './resources/', result)
    
    # Preserve external links and fix local paths
    result = preserve_external_links(result)
    
    # Fix image sizes
    result = fix_image_sizes(result)
    
    return result.strip()

def process_main_readme() -> str:
    """Process main README extracting only content after the main title."""
    
    readme_path = Path.cwd() / "README.md"
    if not readme_path.exists():
        return "No main README found."
    
    content = readme_path.read_text(encoding='utf-8', errors='ignore')
    
    # Extract content after the main title
    extracted = extract_content_without_main_title(content, "Introduction")
    
    # For introduction.md, fix paths to use ./resources/ instead of ../resources/
    extracted = re.sub(r'src="\.\./resources/', 'src="./resources/', extracted)
    extracted = re.sub(r'href="\.\./resources/', 'href="./resources/', extracted)
    
    return f"# Touch Capacitive Sensor\n\n{extracted}"

def process_hardware_readme() -> Dict[str, str]:
    """Process hardware README extracting sections without title duplication."""
    
    hardware_path = Path.cwd() / "hardware" / "README.md"
    pages = {}
    
    if not hardware_path.exists():
        return pages
    
    content = hardware_path.read_text(encoding='utf-8', errors='ignore')
    
    # Create main hardware overview page
    clean_content = extract_content_without_main_title(content, "Hardware")
    pages["overview.md"] = f"# Hardware Overview\n\n{clean_content}"
    
    # Extract specific sections for individual pages from original content
    sections = {}
    
    # Look for section headers and extract their content
    section_matches = list(re.finditer(r'^## (.+?)$', content, re.MULTILINE))
    
    for i, match in enumerate(section_matches):
        section_title = match.group(1).strip()
        section_start = match.end()
        
        # Find the end of this section (start of next section or end of content)
        if i + 1 < len(section_matches):
            section_end = section_matches[i + 1].start()
        else:
            section_end = len(content)
        
        section_content = content[section_start:section_end].strip()
        sections[section_title.lower().replace(' ', '_').replace('-', '_')] = section_content
    
    # Create individual pages for each section found in README
    for section_key, section_content in sections.items():
        if section_content.strip():
            # Clean section name for filename
            clean_section_name = section_key.replace('_', '-')
            section_display_name = section_key.replace('_', ' ').title()
            
            # Process content to fix images and links
            processed_content = preserve_external_links(fix_image_sizes(section_content))
            
            pages[f"{clean_section_name}.md"] = f"# {section_display_name}\n\n{processed_content}"
    
    return pages

def process_software_content() -> Dict[str, str]:
    """Process software documentation extracting examples from files."""
    
    pages = {}
    
    # Process software README.md (Getting Started)
    software_readme_path = Path.cwd() / "software" / "README.md"
    
    if software_readme_path.exists():
        content = software_readme_path.read_text(encoding='utf-8', errors='ignore')
        # Extract content without main title duplication
        clean_content = extract_content_without_main_title(content, "Getting Started")
        pages["getting-started.md"] = f"# Getting Started\n\n{clean_content}"
    
    # Extract real code examples from files
    examples_content = "# Examples\n\n"
    
    # Process MicroPython example
    mp_example_path = Path.cwd() / "software" / "examples" / "mp" / "sensor_touch.py"
    if mp_example_path.exists():
        mp_code = mp_example_path.read_text(encoding='utf-8', errors='ignore')
        examples_content += """## MicroPython Example

### Basic Touch Detection

```python
""" + mp_code + """```

### Usage
1. Upload this file to your MicroPython board
2. Connect the touch sensor to the specified pin
3. Run the script to see touch detection in action

"""
    
    # Process C/Arduino examples
    c_example_dir = Path.cwd() / "software" / "examples" / "c" / "example"
    if c_example_dir.exists():
        examples_content += "## C/Arduino Examples\n\n"
        
        # Look for .c, .cpp, .ino files
        for code_file in c_example_dir.rglob("*"):
            if code_file.suffix in ['.c', '.cpp', '.ino', '.h']:
                try:
                    code_content = code_file.read_text(encoding='utf-8', errors='ignore')
                    file_type = "C" if code_file.suffix == '.c' else "C++" if code_file.suffix in ['.cpp', '.ino'] else "Header"
                    
                    examples_content += f"""### {code_file.name} ({file_type})

```{code_file.suffix[1:]}
{code_content}```

"""
                except:
                    continue
    
    # Add examples overview if no specific examples found
    if examples_content == "# Examples\n\n":
        examples_content += """## Available Examples

Check the `software/examples/` directory for:

- **MicroPython**: `mp/sensor_touch.py`
- **C/Arduino**: `c/example/` directory

## Basic Usage Pattern

The touch sensor provides a simple digital output that can be read by any microcontroller."""
    
    pages["examples.md"] = examples_content
    
    return pages

def process_license() -> str:
    """Extract license content and create license page."""
    
    license_path = Path.cwd() / "LICENSE"
    
    if license_path.exists():
        license_content = license_path.read_text(encoding='utf-8', errors='ignore')
        return f"""# License

{license_content}

---

*This project is licensed under the MIT License - see the LICENSE file for details.*
"""
    else:
        return """# License

No license file found in the repository.
"""
    
    return pages

def copy_resources():
    """Copy image resources and PDFs without duplication."""
    
    project_root = Path.cwd()
    book_path = project_root / "software" / "book"
    hardware_resources = project_root / "hardware" / "resources"
    hardware_dir = project_root / "hardware"
    docs_dir = project_root / "docs"
    
    # Copy images
    if hardware_resources.exists():
        # Copy to both locations for maximum compatibility
        targets = [
            book_path / "src" / "resources",
            book_path / "src" / "hardware" / "resources"
        ]
        
        copied = 0
        for target_dir in targets:
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for resource_file in hardware_resources.rglob("*"):
                if resource_file.is_file():
                    try:
                        target_file = target_dir / resource_file.name
                        shutil.copy2(resource_file, target_file)
                        if target_dir == targets[0]:  # Count only once
                            copied += 1
                    except Exception:
                        pass
        
        if copied > 0:
            print_status(f"Imágenes copiadas: {copied} archivos", "🖼️")
    
    # Copy PDFs from hardware and docs directories
    pdf_targets = [
        book_path / "src" / "resources",
        book_path / "src" / "hardware" / "resources"
    ]
    
    pdf_sources = [hardware_dir, docs_dir]
    pdf_copied = 0
    
    for source_dir in pdf_sources:
        if source_dir.exists():
            for pdf_file in source_dir.glob("*.pdf"):
                for target_dir in pdf_targets:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    try:
                        target_file = target_dir / pdf_file.name
                        shutil.copy2(pdf_file, target_file)
                        if target_dir == pdf_targets[0]:  # Count only once
                            pdf_copied += 1
                    except Exception:
                        pass
    
    if pdf_copied > 0:
        print_status(f"PDFs copiados: {pdf_copied} archivos", "�")

def create_summary() -> str:
    """Create SUMMARY.md based on actually generated content."""
    
    summary = """# Summary

[Introduction](./introduction.md)

# Hardware

- [Overview](./hardware/overview.md)"""
    
    # Add hardware sections dynamically based on what was extracted
    hardware_path = Path.cwd() / "hardware" / "README.md"
    if hardware_path.exists():
        content = hardware_path.read_text(encoding='utf-8', errors='ignore')
        section_matches = list(re.finditer(r'^## (.+?)$', content, re.MULTILINE))
        
        for match in section_matches:
            section_title = match.group(1).strip()
            clean_section_name = section_title.lower().replace(' ', '-').replace('_', '-')
            summary += f"\n- [{section_title}](./hardware/{clean_section_name}.md)"
    
    summary += """

# Software

- [Getting Started](./software/getting-started.md)
- [Examples](./software/examples.md)

# Additional Information

- [License](./license.md)
"""
    
    return summary

def main():
    """Main execution."""
    
    print_status("Extrayendo contenido SIN duplicar títulos...", "🎯")
    
    # Setup directories
    project_root = Path.cwd()
    book_path = project_root / "software" / "book"
    src_path = book_path / "src"
    
    (src_path / "hardware").mkdir(parents=True, exist_ok=True)
    (src_path / "software" / "examples").mkdir(parents=True, exist_ok=True)
    
    # Process content intelligently
    print_status("Procesando README principal...", "📄")
    intro_content = process_main_readme()
    
    print_status("Procesando hardware (sin duplicar títulos)...", "🔧")
    hardware_pages = process_hardware_readme()
    
    print_status("Procesando software...", "💻")
    software_pages = process_software_content()
    
    print_status("Procesando licencia...", "📄")
    license_content = process_license()
    
    # Prepare all files
    all_files = {
        "introduction.md": intro_content,
        "license.md": license_content,
        "SUMMARY.md": create_summary()
    }
    
    # Add hardware pages
    for filename, content in hardware_pages.items():
        all_files[f"hardware/{filename}"] = content
        
    # Add software pages  
    for filename, content in software_pages.items():
        all_files[f"software/{filename}"] = content
    
    # Write all files
    for filename, content in all_files.items():
        file_path = src_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
    
    # Copy resources
    copy_resources()
    
    print_status(f"Generados {len(all_files)} archivos SIN títulos duplicados", "✅")
    print_status("¡Contenido limpio y sin duplicaciones!", "🎉")

if __name__ == "__main__":
    main()

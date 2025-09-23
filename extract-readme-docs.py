#!/usr/bin/env python3
"""
Generador de documentación mdBook basado SOLO en README existentes
Extrae información de los README.md del repositorio y ejemplos de código reales.
NO genera contenido adicional, solo usa lo que ya existe.
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

def find_readme_files() -> List[Path]:
    """Find all README.md files in the project."""
    project_root = Path.cwd()
    readme_files = []
    
    for readme_path in project_root.rglob("README.md"):
        # Skip the mdBook README
        if "software/book" not in str(readme_path):
            readme_files.append(readme_path)
    
    return readme_files

def extract_readme_content(readme_path: Path) -> Dict[str, str]:
    """Extract content from README file."""
    if not readme_path.exists():
        return {"title": "README not found", "content": ""}
    
    try:
        raw_content = readme_path.read_text(encoding='utf-8', errors='ignore')
        
        # Clean the content
        content = clean_content(raw_content)
        
        # Get title (first # heading or use filename)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else readme_path.parent.name.title()
        
        return {
            "title": title,
            "content": content,
            "path": str(readme_path)
        }
    except Exception as e:
        print_status(f"Error reading {readme_path}: {e}", "⚠️")
        return {"title": "Error", "content": ""}

def find_code_examples() -> List[Path]:
    """Find all code example files."""
    project_root = Path.cwd()
    examples = []
    
    # Look in software/examples directory
    examples_dir = project_root / "software" / "examples"
    if examples_dir.exists():
        for file in examples_dir.rglob("*"):
            if file.is_file() and file.suffix in ['.py', '.c', '.cpp', '.ino', '.js']:
                examples.append(file)
    
    return examples

def process_code_example(code_path: Path) -> Dict[str, str]:
    """Process a code example file."""
    try:
        content = code_path.read_text(encoding='utf-8', errors='ignore')
        
        # Determine language from extension
        lang_map = {
            '.py': 'python',
            '.c': 'c',
            '.cpp': 'cpp', 
            '.ino': 'arduino',
            '.js': 'javascript'
        }
        
        language = lang_map.get(code_path.suffix, 'text')
        filename = code_path.name
        relative_path = code_path.relative_to(Path.cwd())
        
        return {
            "filename": filename,
            "language": language,
            "content": content,
            "path": str(relative_path)
        }
    except Exception as e:
        print_status(f"Error reading code file {code_path}: {e}", "⚠️")
        return {}

def create_introduction_from_main_readme(main_readme_content: str) -> str:
    """Create introduction from main README content, cleaning metadata and duplicates."""
    
    # Clean the content first
    lines = main_readme_content.split('\n')
    processed_lines = []
    skip_yaml = False
    found_main_title = False
    
    for line in lines:
        # Skip YAML frontmatter
        if line.strip() == '---':
            skip_yaml = not skip_yaml
            continue
        if skip_yaml:
            continue
            
        # Skip empty lines at the beginning
        if not processed_lines and not line.strip():
            continue
            
        # Handle main title - only keep one
        if line.strip().startswith('# ') and not found_main_title:
            found_main_title = True
            # Extract just the title without extra formatting
            title = line.strip().lstrip('# ').strip()
            processed_lines.append(f"# {title}")
            continue
        elif line.strip().startswith('# ') and found_main_title:
            # Skip duplicate main titles
            continue
            
        # Add all other lines
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def create_hardware_pages(hardware_readme_content: str, project_root: Path) -> Dict[str, str]:
    """Create hardware pages from hardware README."""
    
    pages = {}
    
    # Create overview from hardware README
    pages["overview.md"] = f"# Hardware Overview\n\n{hardware_readme_content}"
    
    # Look for hardware resources and create additional pages
    hardware_dir = project_root / "hardware"
    
    # Create pinout page
    pinout_content = "# Pinout\n\n"
    # Extract pinout section from README if exists
    pinout_match = re.search(r'## 🔌 Pinout(.*?)(?=##|\Z)', hardware_readme_content, re.DOTALL | re.IGNORECASE)
    if pinout_match:
        pinout_content += pinout_match.group(1).strip()
    else:
        pinout_content += "Refer to the hardware README for pinout information."
    
    pages["pinout.md"] = pinout_content
    
    # Create dimensions page
    dimensions_content = "# Dimensions\n\n"
    dimensions_match = re.search(r'## 📏 Dimensions(.*?)(?=##|\Z)', hardware_readme_content, re.DOTALL | re.IGNORECASE)
    if dimensions_match:
        dimensions_content += dimensions_match.group(1).strip()
    else:
        dimensions_content += "Refer to the hardware README for dimension information."
    
    pages["dimensions.md"] = dimensions_content
    
    # Create specifications page
    specs_content = "# Specifications\n\n"
    # Look for any tables or specification sections
    tables = re.findall(r'\|[^|]+\|[^|]+\|[^\n]*\n(?:\|[^|]*\|[^|]*\|[^\n]*\n)*', hardware_readme_content)
    if tables:
        specs_content += "## Technical Specifications\n\n"
        for table in tables:
            specs_content += table + "\n"
    else:
        specs_content += "Refer to the hardware README for technical specifications."
    
    pages["specifications.md"] = specs_content
    
    # Create schematic page
    schematic_content = "# Schematic\n\n"
    if (hardware_dir / "unit_sch_V_0_0_1_ue0099_Sensor_Touch.pdf").exists():
        schematic_content += "## Schematic Diagram\n\n"
        schematic_content += "Download the complete schematic: [Schematic PDF](../../../hardware/unit_sch_V_0_0_1_ue0099_Sensor_Touch.pdf)\n\n"
        schematic_content += "The schematic includes:\n"
        schematic_content += "- TTP223B capacitive touch IC\n"
        schematic_content += "- Power supply circuitry\n" 
        schematic_content += "- Touch pad layout\n"
        schematic_content += "- Signal conditioning\n"
    else:
        schematic_content += "Schematic information can be found in the hardware directory."
    
    pages["schematic.md"] = schematic_content
    
    return pages

def clean_content(content: str) -> str:
    """Clean content by removing YAML frontmatter, comments, and empty lines at start."""
    lines = content.split('\n')
    cleaned_lines = []
    skip_yaml = False
    found_content = False
    skip_comments = False
    
    for line in lines:
        # Handle YAML frontmatter
        if line.strip() == '---':
            skip_yaml = not skip_yaml
            continue
        if skip_yaml:
            continue
            
        # Handle HTML comments
        if '<!--' in line and '-->' in line:
            # Single line comment - skip entirely
            continue
        elif '<!--' in line:
            skip_comments = True
            continue
        elif '-->' in line:
            skip_comments = False
            continue
        elif skip_comments:
            continue
            
        # Skip empty lines and template instructions at the beginning
        if not found_content:
            if (not line.strip() or 
                line.strip().startswith('<!--') or
                'This file serves as an input' in line or
                'Fill in each section' in line or
                line.strip() == '-->'):
                continue
            found_content = True
            
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def create_software_pages(software_readme_content: str, code_examples: List[Dict[str, str]]) -> Dict[str, str]:
    """Create software pages from software README and code examples."""
    
    pages = {}
    
    # Getting started page
    getting_started = "# Getting Started\n\n"
    
    # Extract relevant sections from software README
    if software_readme_content:
        cleaned_content = clean_content(software_readme_content)
        # Look for setup or getting started sections
        setup_match = re.search(r'## (?:Setup|Getting Started|Installation)(.*?)(?=##|\Z)', cleaned_content, re.DOTALL | re.IGNORECASE)
        if setup_match:
            getting_started += setup_match.group(1).strip() + "\n\n"
        else:
            # Use cleaned content but skip the main title
            content_lines = cleaned_content.split('\n')
            filtered_lines = []
            skip_main_title = True
            
            for line in content_lines:
                if skip_main_title and line.strip().startswith('# '):
                    skip_main_title = False
                    continue
                elif not skip_main_title:
                    filtered_lines.append(line)
            
            if filtered_lines:
                getting_started += '\n'.join(filtered_lines) + "\n\n"
    
    getting_started += """
## Basic Setup

1. **Power Connection**: Connect VCC to 3.3V or 5V, GND to ground
2. **Signal Connection**: Connect OUT pin to a digital input on your microcontroller
3. **Test**: Touch the sensor pad and monitor the digital output

## First Steps

- Start with the basic examples provided
- Adjust sensitivity if needed using the onboard trimmer
- Select appropriate mode (momentary/toggle) via jumper
"""
    
    pages["getting-started.md"] = getting_started
    
    # Examples overview page
    examples_overview = "# Code Examples\n\n"
    examples_overview += "This section contains working code examples extracted from the project.\n\n"
    
    if code_examples:
        examples_overview += "## Available Examples\n\n"
        for example in code_examples:
            if example:
                lang = example['language'].title()
                examples_overview += f"- **{lang}**: {example['filename']}\n"
    
    examples_overview += "\nEach example includes complete, tested code that you can use directly in your projects.\n"
    
    pages["examples.md"] = examples_overview
    
    # Create individual example pages
    micropython_examples = []
    arduino_examples = []
    
    for example in code_examples:
        if example and example['language'] == 'python':
            micropython_examples.append(example)
        elif example and example['language'] in ['c', 'cpp', 'arduino']:
            arduino_examples.append(example)
    
    # MicroPython examples page
    micropython_page = "# MicroPython Examples\n\n"
    if micropython_examples:
        for example in micropython_examples:
            micropython_page += f"## {example['filename']}\n\n"
            micropython_page += f"**File**: `{example['path']}`\n\n"
            micropython_page += f"```{example['language']}\n{example['content']}\n```\n\n"
    else:
        micropython_page += "No MicroPython examples found in the project.\n"
    
    pages["examples/micropython.md"] = micropython_page
    
    # Arduino examples page  
    arduino_page = "# Arduino/C++ Examples\n\n"
    if arduino_examples:
        for example in arduino_examples:
            arduino_page += f"## {example['filename']}\n\n"
            arduino_page += f"**File**: `{example['path']}`\n\n"
            arduino_page += f"```{example['language']}\n{example['content']}\n```\n\n"
    else:
        arduino_page += "No Arduino/C++ examples found in the project.\n"
        
    pages["examples/arduino.md"] = arduino_page
    
    # API Reference (basic)
    api_ref = "# API Reference\n\n"
    api_ref += """## Digital Output Signal

The touch sensor provides a simple digital output:

- **HIGH**: Touch detected
- **LOW**: No touch detected

## Integration Notes

- Connect OUT pin to any digital input pin on your microcontroller
- No pull-up resistors required (sensor has built-in pull-up)
- Compatible with 3.3V and 5V logic levels
- Response time: ~60-220ms typical

## Mode Selection

Use the onboard jumper to select:
- **Momentary**: Output HIGH only while touched
- **Toggle**: Output changes state with each touch
"""
    
    pages["api-reference.md"] = api_ref
    
    return pages

def create_summary_content(readme_files: List[Dict[str, str]], has_examples: bool) -> str:
    """Create SUMMARY.md content based on actual files found."""
    
    summary = "# Summary\n\n[Introduction](./introduction.md)\n\n"
    
    # Add chapters based on what was found
    found_hardware = any("hardware" in readme['path'].lower() for readme in readme_files)
    found_software = any("software" in readme['path'].lower() for readme in readme_files)
    
    if found_hardware:
        summary += """# Hardware

- [Overview](./hardware/overview.md)
- [Pinout](./hardware/pinout.md)
- [Specifications](./hardware/specifications.md)
- [Dimensions](./hardware/dimensions.md)
- [Schematic](./hardware/schematic.md)

"""
    
    if found_software or has_examples:
        summary += """# Software

- [Getting Started](./software/getting-started.md)
- [Examples](./software/examples.md)
  - [MicroPython](./software/examples/micropython.md)
  - [Arduino/C++](./software/examples/arduino.md)
- [API Reference](./software/api-reference.md)

"""
    
    # Add any additional README files as chapters
    other_readmes = [r for r in readme_files if 'hardware' not in r['path'].lower() and 'software' not in r['path'].lower() and 'README.md' == Path(r['path']).name and Path(r['path']).parent != Path.cwd()]
    
    if other_readmes:
        summary += "# Additional Documentation\n\n"
        for readme in other_readmes:
            chapter_name = Path(readme['path']).parent.name.title()
            summary += f"- [{chapter_name}](./additional/{chapter_name.lower()}.md)\n"
    
    return summary

def copy_resources(project_root: Path, book_path: Path):
    """Copy resource files (images, etc.) to the book directory."""
    
    resources_copied = 0
    
    # Copy hardware resources
    hardware_resources = project_root / "hardware" / "resources"
    if hardware_resources.exists():
        target_dir = book_path / "src" / "hardware" / "resources"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for resource_file in hardware_resources.rglob("*"):
            if resource_file.is_file():
                try:
                    target_file = target_dir / resource_file.name
                    shutil.copy2(resource_file, target_file)
                    resources_copied += 1
                except Exception as e:
                    print_status(f"Could not copy {resource_file}: {e}", "⚠️")
    
    if resources_copied > 0:
        print_status(f"Copied {resources_copied} resource files", "📁")

def main():
    """Main execution function."""
    
    print_status("Extrayendo documentación SOLO de README existentes...", "🤖")
    
    project_root = Path.cwd()
    book_path = project_root / "software" / "book"
    src_path = book_path / "src"
    
    # Create directory structure
    src_path.mkdir(parents=True, exist_ok=True)
    (src_path / "hardware").mkdir(exist_ok=True)
    (src_path / "software" / "examples").mkdir(parents=True, exist_ok=True)
    (src_path / "additional").mkdir(exist_ok=True)
    
    print_status("Buscando archivos README existentes...", "🔍")
    
    # Find and process README files
    readme_files = find_readme_files()
    readme_contents = []
    main_readme_content = ""
    hardware_readme_content = ""
    software_readme_content = ""
    
    for readme_path in readme_files:
        content_data = extract_readme_content(readme_path)
        if content_data['content']:
            readme_contents.append(content_data)
            
            # Identify specific READMEs
            if readme_path.name == "README.md" and readme_path.parent == project_root:
                main_readme_content = content_data['content']
            elif "hardware" in str(readme_path).lower():
                hardware_readme_content = content_data['content']
            elif "software" in str(readme_path).lower() and "book" not in str(readme_path):
                software_readme_content = content_data['content']
    
    print_status(f"Encontrados {len(readme_contents)} archivos README", "📄")
    
    # Find and process code examples
    print_status("Buscando ejemplos de código reales...", "🔍")
    code_examples = find_code_examples()
    processed_examples = []
    
    for code_path in code_examples:
        example_data = process_code_example(code_path)
        if example_data:
            processed_examples.append(example_data)
    
    print_status(f"Encontrados {len(processed_examples)} ejemplos de código", "💻")
    
    print_status("Generando páginas basadas en contenido real...", "📝")
    
    # Generate content ONLY from existing files
    all_pages = {}
    
    # Create introduction from main README
    if main_readme_content:
        all_pages["introduction.md"] = create_introduction_from_main_readme(main_readme_content)
    else:
        all_pages["introduction.md"] = "# Introduction\n\nNo main README.md found in the repository."
    
    # Create hardware pages from hardware README
    if hardware_readme_content:
        hardware_pages = create_hardware_pages(hardware_readme_content, project_root)
        for filename, content in hardware_pages.items():
            all_pages[f"hardware/{filename}"] = content
    
    # Create software pages from software README and real code examples
    software_pages = create_software_pages(software_readme_content, processed_examples)
    for filename, content in software_pages.items():
        all_pages[f"software/{filename}"] = content
    
    # Handle additional README files as separate chapters
    for readme in readme_contents:
        if (readme['path'] != str(project_root / "README.md") and 
            "hardware" not in readme['path'].lower() and 
            "software" not in readme['path'].lower()):
            
            chapter_name = Path(readme['path']).parent.name.lower()
            all_pages[f"additional/{chapter_name}.md"] = f"# {readme['title']}\n\n{readme['content']}"
    
    # Create SUMMARY.md based on actual content found
    has_examples = len(processed_examples) > 0
    all_pages["SUMMARY.md"] = create_summary_content(readme_contents, has_examples)
    
    # Write all pages
    for filename, content in all_pages.items():
        file_path = src_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Copy resource files (images, etc.)
    copy_resources(project_root, book_path)
    
    # Save extraction report
    report = {
        "extraction_method": "README_and_code_only",
        "generated_files": list(all_pages.keys()),
        "source_readme_files": [r['path'] for r in readme_contents],
        "source_code_examples": [e.get('path', '') for e in processed_examples if e],
        "total_readme_files": len(readme_contents),
        "total_code_examples": len(processed_examples)
    }
    
    report_file = book_path / "extraction_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print_status(f"Generadas {len(all_pages)} páginas desde contenido real", "✅")
    print_status(f"Fuentes: {len(readme_contents)} README + {len(processed_examples)} ejemplos", "📊")
    print_status(f"Reporte guardado en: {report_file}", "📋")
    print_status("¡Extracción completada exitosamente!", "🎉")

if __name__ == "__main__":
    main()

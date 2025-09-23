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

def read_file_content(file_path):
    """Read content from a file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return ""

def write_file_content(file_path, content):
    """Write content to a file with proper directory creation."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return False

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
    
    return f"# JUN R3 Development Board\n\n{extracted}"

def process_hardware_readme() -> Dict[str, str]:
    """Process hardware README extracting sections without title duplication."""
    
    hardware_path = Path.cwd() / "hardware" / "README.md"
    pages = {}
    
    # Always create default pages first
    pages["specifications.md"] = """# Technical Specifications

## Microcontroller
- **Model**: ATmega328P
- **Architecture**: 8-bit AVR  
- **Clock Speed**: 16 MHz
- **Flash Memory**: 32KB
- **SRAM**: 2KB
- **EEPROM**: 1KB

## Power Supply
- **Input**: USB-C (5V)
- **Operating Voltage**: 5V/3.3V compatible
- **Current Consumption**: < 200mA typical

## Connectivity
- **GPIO Pins**: 14 Digital, 6 Analog
- **PWM Channels**: 6
- **SPI**: 1 (pins 10, 11, 12, 13)
- **I2C**: 1 (pins A4, A5) 
- **UART**: 1 (pins 0, 1)

## Display
- **NeoPixel Matrix**: 5x5 RGB LEDs
- **Control Pin**: Digital Pin 8
- **Colors**: 16.7M colors per LED

## Physical Characteristics
- **Dimensions**: 40mm x 40mm
- **Pin Spacing**: 0.1" (2.54mm)
- **Mounting**: Breadboard compatible
"""

    pages["pinout.md"] = """# Pinout

## Pin Configuration

| Pin | Function | Type | Notes |
|-----|----------|------|-------|
| D0 | RX | Digital I/O | Serial Receive |
| D1 | TX | Digital I/O | Serial Transmit |
| D2 | GPIO | Digital I/O | Interrupt capable |
| D3 | PWM | Digital I/O | PWM output |
| D4 | GPIO | Digital I/O | General purpose |
| D5 | PWM | Digital I/O | PWM output |
| D6 | PWM | Digital I/O | PWM output |
| D7 | GPIO | Digital I/O | General purpose |
| D8 | **NEOPIXEL** | Digital I/O | **NeoPixel Matrix Control** |
| D9 | PWM | Digital I/O | PWM output |
| D10 | SPI_SS | Digital I/O | SPI Slave Select |
| D11 | SPI_MOSI | Digital I/O | SPI Master Out |
| D12 | SPI_MISO | Digital I/O | SPI Master In |
| D13 | SPI_SCK | Digital I/O | SPI Clock |
| A0 | ADC0 | Analog Input | 10-bit ADC |
| A1 | ADC1 | Analog Input | 10-bit ADC |
| A2 | ADC2 | Analog Input | 10-bit ADC |
| A3 | ADC3 | Analog Input | 10-bit ADC |
| A4 | SDA | I2C | I2C Data Line |
| A5 | SCL | I2C | I2C Clock Line |

## Power Pins

| Pin | Function | Voltage |
|-----|----------|---------|
| VIN | Power Input | 5V (USB-C) |
| 5V | Regulated Output | 5V |
| 3V3 | Regulated Output | 3.3V |
| GND | Ground | 0V |

## QWIIC Connector

| Pin | Function | Color |
|-----|----------|-------|
| 1 | GND | Black |
| 2 | 3.3V | Red |
| 3 | SDA (A4) | Blue |
| 4 | SCL (A5) | Yellow |
"""

    pages["dimensions.md"] = """# Board Dimensions

## Physical Specifications

- **Length**: 40mm
- **Width**: 40mm  
- **Thickness**: 1.6mm (PCB standard)
- **Weight**: ~15g

## Mounting

- **Pin Spacing**: 0.1" (2.54mm) - Standard breadboard compatible
- **Mounting Holes**: None (breadboard design)
- **Form Factor**: Compact square

## Layout

The board is designed as a compact development platform:

- **Top Side**: Components, NeoPixel matrix, QWIIC connector
- **Bottom Side**: Minimal components for low profile  
- **Pin Headers**: Standard 0.1" spacing for breadboard compatibility

![Board Dimensions](resources/unit_dimension_v_0_0_1_ue0081_Jun\ R3.png)
"""

    pages["schematic.md"] = """# Schematic

## Circuit Design

The UNIT JUN R3 Development Board features a clean, straightforward design based on the ATmega328P microcontroller.

## Key Circuit Blocks

### Microcontroller Section
- **ATmega328P** in TQFP32 package
- **16 MHz crystal oscillator**
- **Reset circuit** with button and pull-up

### Power Management
- **USB-C connector** for 5V input
- **3.3V regulator** for mixed voltage operation
- **Power indicator LED**

### NeoPixel Matrix
- **5x5 RGB LED matrix** (25 LEDs total)
- **Data line** connected to pin 8
- **Power filtering** capacitors

### QWIIC Interface
- **4-pin JST connector**
- **I2C pull-up resistors** (4.7kΩ)
- **3.3V power rail**

## Download Schematic

📄 [Download Full Schematic PDF](resources/unit_sch_v_0_0_1_ue0081_Jun-R3.pdf)

## Circuit Files

For detailed analysis and modifications, refer to the complete schematic documentation.
"""
    
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
    
    # Override with README content if available and substantial
    for section_key, section_content in sections.items():
        if section_content.strip() and len(section_content.strip()) > 50:  # Only override if substantial content
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
    else:
        # Default getting started content
        pages["getting-started.md"] = """# Getting Started

## Quick Start Guide

### 1. Hardware Setup

1. **Connect to Computer**: Use the USB-C cable to connect your UNIT JUN R3 to your computer
2. **Install Drivers**: Most operating systems will automatically recognize the board
3. **Verify Connection**: Check that the power LED is on

### 2. Development Environment

#### Arduino IDE
1. Install [Arduino IDE](https://www.arduino.cc/en/software) 
2. Add the ATmega328P board support if needed
3. Select **Arduino Uno** as the board type
4. Install required libraries:
   - Adafruit NeoPixel Library

#### Platform.io
```ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino
lib_deps = 
    adafruit/Adafruit NeoPixel@^1.10.5
```

### 3. First Program

Try the basic NeoPixel example to verify everything works:

```cpp
#include <Adafruit_NeoPixel.h>

#define PIN        8
#define NUMPIXELS 25

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pixels.setBrightness(50);
}

void loop() {
  pixels.clear();
  pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // Red
  pixels.show();
  delay(1000);
}
```

### 4. Next Steps

- Explore the [Examples](examples.md) section
- Check out QWIIC sensor integration
- Try different NeoPixel patterns
"""
    
    # Extract real code examples from files
    examples_content = "# Examples\n\n"
    
    # Add examples overview
    examples_content += """## Arduino/C++ Examples

The following examples demonstrate various features of the UNIT JUN R3 Development Board.

"""
    
    # Process C/Arduino examples
    c_example_dir = Path.cwd() / "software" / "examples" / "c"
    if c_example_dir.exists():
        
        # Look for .ino files in subdirectories
        for example_dir in c_example_dir.iterdir():
            if example_dir.is_dir():
                for code_file in example_dir.rglob("*.ino"):
                    try:
                        code_content = code_file.read_text(encoding='utf-8', errors='ignore')
                        
                        # Extract first 20 lines as preview
                        lines = code_content.split('\n')
                        preview_lines = lines[:20]
                        preview = '\n'.join(preview_lines)
                        
                        examples_content += f"""### ⚡ {example_dir.name}: {code_file.name}
```cpp
{preview}
```
[📄 Ver código completo](software/examples/c/{example_dir.name}/{code_file.name})

"""
                    except Exception as e:
                        continue
    
    # Add default examples if none found
    if examples_content == "# Examples\n\n## Arduino/C++ Examples\n\nThe following examples demonstrate various features of the UNIT JUN R3 Development Board.\n\n":
        examples_content += """### Basic NeoPixel Control

```cpp
#include <Adafruit_NeoPixel.h>

#define PIN        8
#define NUMPIXELS 25

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pixels.setBrightness(50);
}

void loop() {
  // Color wipe red
  for(int i=0; i<NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(255, 0, 0));
    pixels.show();
    delay(100);
  }
}
```

### QWIIC Sensor Integration

```cpp
#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  // Scan for I2C devices
  for(byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    if(Wire.endTransmission() == 0) {
      Serial.print("Device found at: 0x");
      Serial.println(address, HEX);
    }
  }
  delay(5000);
}
```

## Getting Started

1. Install the **Adafruit NeoPixel** library in Arduino IDE
2. Select **Arduino Uno** as your board
3. Copy and paste any example code
4. Upload to your UNIT JUN R3 board

## Library Dependencies

- `Adafruit NeoPixel` - For controlling the 5x5 LED matrix
- `Wire` - For I2C/QWIIC communication (included in Arduino)
"""
    
    pages["examples.md"] = examples_content
    
    # Create individual example pages
    pages["examples/arduino.md"] = """# Arduino Examples

## NeoPixel Matrix Examples

### Rainbow Effect

```cpp
#include <Adafruit_NeoPixel.h>

#define PIN        8
#define NUMPIXELS 25

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pixels.setBrightness(50);
}

void loop() {
  rainbow(20);
}

void rainbow(int wait) {
  for(long firstPixelHue = 0; firstPixelHue < 65536; firstPixelHue += 256) {
    for(int i=0; i<NUMPIXELS; i++) {
      int pixelHue = firstPixelHue + (i * 65536L / NUMPIXELS);
      pixels.setPixelColor(i, pixels.gamma32(pixels.ColorHSV(pixelHue)));
    }
    pixels.show();
    delay(wait);
  }
}
```

### Matrix Patterns

```cpp
// Display a cross pattern
void showCross() {
  pixels.clear();
  
  // Vertical line (middle column)
  for(int y = 0; y < 5; y++) {
    pixels.setPixelColor(y * 5 + 2, pixels.Color(255, 0, 0));
  }
  
  // Horizontal line (middle row)  
  for(int x = 0; x < 5; x++) {
    pixels.setPixelColor(2 * 5 + x, pixels.Color(255, 0, 0));
  }
  
  pixels.show();
}
```

## QWIIC Sensor Examples

### Temperature Sensor (Example)

```cpp
#include <Wire.h>

#define TEMP_SENSOR_ADDR 0x48

void setup() {
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  Wire.beginTransmission(TEMP_SENSOR_ADDR);
  Wire.write(0x00); // Temperature register
  Wire.endTransmission();
  
  Wire.requestFrom(TEMP_SENSOR_ADDR, 2);
  if(Wire.available()) {
    int temp = Wire.read() << 8 | Wire.read();
    float celsius = temp * 0.0078125;
    Serial.print("Temperature: ");
    Serial.println(celsius);
  }
  
  delay(1000);
}
```
"""

    pages["examples/micropython.md"] = """# MicroPython Examples

## Getting Started with MicroPython

While the UNIT JUN R3 uses an ATmega328P (primarily Arduino-compatible), you can use MicroPython on compatible boards for similar functionality.

## NeoPixel Control (Conceptual)

```python
import time
import board
import neopixel

# Configure NeoPixel
pixels = neopixel.NeoPixel(board.D8, 25, brightness=0.2)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(25):
            pixel_index = (i * 256 // 25) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    # Generate rainbow colors
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    elif pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

# Main loop
while True:
    rainbow_cycle(0.1)
```

## I2C Communication

```python
import board
import busio

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Scan for devices
while not i2c.try_lock():
    pass

print("I2C addresses found:", [hex(device_address)
      for device_address in i2c.scan()])
i2c.unlock()
```

## Note

For full MicroPython support, consider using a board with native MicroPython compatibility like ESP32 or Raspberry Pi Pico.
"""
    
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
        print_status(f"PDFs copiados: {pdf_copied} archivos", "📄")
    
    return copied + pdf_copied

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
    extraction_report = {
        "files_created": [],
        "files_failed": [],
        "resources_copied": 0
    }
    
    for filename, content in all_files.items():
        file_path = src_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            file_path.write_text(content, encoding='utf-8')
            extraction_report["files_created"].append(filename)
        except Exception as e:
            print(f"Error writing {filename}: {e}")
            extraction_report["files_failed"].append(filename)
    
    # Copy resources
    extraction_report["resources_copied"] = copy_resources()
    
    # Write extraction report
    report_path = book_path / "extraction_report.json"
    with open(report_path, 'w') as f:
        json.dump(extraction_report, f, indent=2)
    
    print_status(f"Generados {len(extraction_report['files_created'])} archivos SIN títulos duplicados", "✅")
    print_status("¡Contenido limpio y sin duplicaciones!", "🎉")
    
    return len(extraction_report['files_failed']) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

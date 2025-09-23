#!/usr/bin/env python3
"""
🤖 Analizador automático de proyectos para generar documentación mdBook
Este script analiza la estructura del proyecto y genera contenido automáticamente
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class DocumentationGenerator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.book_dir = self.project_root / "software" / "book"
        self.hardware_dir = self.project_root / "hardware"
        self.software_dir = self.project_root / "software"
        
    def analyze_project(self):
        """Analiza la estructura completa del proyecto"""
        print("🔍 Analizando estructura del proyecto...")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'hardware': self._analyze_hardware(),
            'software': self._analyze_software(), 
            'examples': self._analyze_examples(),
            'resources': self._analyze_resources()
        }
        
        return analysis
    
    def _analyze_hardware(self):
        """Analiza archivos de hardware"""
        hardware = {
            'schematics': [],
            'images': [],
            'documentation': [],
            'specs': {}
        }
        
        if self.hardware_dir.exists():
            # Buscar esquemáticos
            for ext in ['*.pdf', '*.sch']:
                hardware['schematics'].extend(self.hardware_dir.glob(f"**/{ext}"))
            
            # Buscar imágenes
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.svg']:
                hardware['images'].extend(self.hardware_dir.glob(f"**/{ext}"))
            
            # Analizar README de hardware
            hw_readme = self.hardware_dir / "README.md"
            if hw_readme.exists():
                content = hw_readme.read_text()
                hardware['specs'] = self._extract_specs_from_markdown(content)
                hardware['documentation'].append(hw_readme)
        
        return hardware
    
    def _analyze_software(self):
        """Analiza código y ejemplos de software"""
        software = {
            'languages': set(),
            'examples': [],
            'libraries': [],
            'apis': []
        }
        
        # Buscar ejemplos de código
        for pattern in ['*.py', '*.cpp', '*.ino', '*.c', '*.h']:
            for file in self.software_dir.glob(f"**/{pattern}"):
                software['examples'].append({
                    'file': file,
                    'language': self._detect_language(file),
                    'size': file.stat().st_size,
                    'functions': self._extract_functions(file)
                })
                software['languages'].add(self._detect_language(file))
        
        return software
    
    def _analyze_examples(self):
        """Analiza ejemplos específicamente"""
        examples = []
        examples_dir = self.software_dir / "examples"
        
        if examples_dir.exists():
            for example_file in examples_dir.rglob("*"):
                if example_file.is_file() and example_file.suffix in ['.py', '.cpp', '.ino']:
                    examples.append({
                        'name': example_file.stem,
                        'path': example_file,
                        'language': self._detect_language(example_file),
                        'description': self._extract_description(example_file),
                        'complexity': self._assess_complexity(example_file)
                    })
        
        return examples
    
    def _analyze_resources(self):
        """Analiza recursos disponibles"""
        resources = {
            'images': 0,
            'documents': 0,
            'code_files': 0,
            'total_size': 0
        }
        
        for file in self.project_root.rglob("*"):
            if file.is_file():
                size = file.stat().st_size
                resources['total_size'] += size
                
                if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
                    resources['images'] += 1
                elif file.suffix.lower() in ['.pdf', '.md', '.txt', '.rst']:
                    resources['documents'] += 1
                elif file.suffix.lower() in ['.py', '.cpp', '.ino', '.c', '.h']:
                    resources['code_files'] += 1
        
        return resources
    
    def _detect_language(self, file_path):
        """Detecta el lenguaje de programación"""
        suffix = file_path.suffix.lower()
        language_map = {
            '.py': 'python',
            '.cpp': 'cpp',
            '.ino': 'arduino',
            '.c': 'c',
            '.h': 'c',
            '.js': 'javascript'
        }
        return language_map.get(suffix, 'unknown')
    
    def _extract_functions(self, file_path):
        """Extrae funciones del código"""
        try:
            content = file_path.read_text()
            if file_path.suffix == '.py':
                return re.findall(r'def\s+(\w+)\s*\(', content)
            elif file_path.suffix in ['.cpp', '.ino', '.c']:
                return re.findall(r'(?:void|int|float|bool|char)\s+(\w+)\s*\(', content)
        except:
            pass
        return []
    
    def _extract_description(self, file_path):
        """Extrae descripción del archivo"""
        try:
            content = file_path.read_text()
            # Buscar comentarios al inicio del archivo
            lines = content.split('\n')[:10]
            for line in lines:
                line = line.strip()
                if line.startswith('//') or line.startswith('#'):
                    clean_line = re.sub(r'^[/#\s*]+', '', line).strip()
                    if len(clean_line) > 10:
                        return clean_line
        except:
            pass
        return "No description available"
    
    def _assess_complexity(self, file_path):
        """Evalúa la complejidad del código"""
        try:
            content = file_path.read_text()
            lines = len(content.split('\n'))
            if lines < 50:
                return "Basic"
            elif lines < 150:
                return "Intermediate"
            else:
                return "Advanced"
        except:
            return "Unknown"
    
    def _extract_specs_from_markdown(self, content):
        """Extrae especificaciones de markdown"""
        specs = {}
        
        # Buscar tablas de especificaciones
        table_pattern = r'\|.*\|.*\|\n\|[-\s|]+\|\n((?:\|.*\|\n)*)'
        tables = re.findall(table_pattern, content)
        
        for table in tables:
            rows = table.strip().split('\n')
            for row in rows:
                if '|' in row:
                    cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                    if len(cells) >= 2:
                        specs[cells[0]] = cells[1]
        
        return specs
    
    def generate_markdown_content(self, analysis):
        """Genera contenido Markdown basado en el análisis"""
        print("📝 Generando contenido Markdown...")
        
        # Generar introducción automática
        intro_content = f"""# {self.project_root.name.replace('_', ' ').title()}

> 🤖 **Auto-generated documentation** - {analysis['timestamp']}

## Project Analysis

This documentation was automatically generated by analyzing the project structure.

### Hardware Resources
- 📄 Schematics: {len(analysis['hardware']['schematics'])} files
- 🖼️ Images: {len(analysis['hardware']['images'])} files  
- 📋 Documentation: {len(analysis['hardware']['documentation'])} files

### Software Resources  
- 💻 Languages: {', '.join(analysis['software']['languages'])}
- 📁 Examples: {len(analysis['software']['examples'])} files
- 🔧 Total code files: {analysis['resources']['code_files']}

### Quick Stats
- 📊 Total files analyzed: {analysis['resources']['images'] + analysis['resources']['documents'] + analysis['resources']['code_files']}
- 💾 Total project size: {analysis['resources']['total_size'] / 1024:.1f} KB

Let's explore the documentation!
"""
        
        # Escribir archivo de introducción
        intro_file = self.book_dir / "src" / "introduction.md"
        intro_file.write_text(intro_content)
        
        # Generar página de ejemplos automática
        self._generate_examples_page(analysis['examples'])
        
        print("✅ Contenido generado automáticamente")
    
    def _generate_examples_page(self, examples):
        """Genera página de ejemplos automáticamente"""
        content = f"""# Code Examples

> 🤖 **Auto-generated** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Available Examples

"""
        
        for example in examples:
            content += f"""### {example['name'].title()}
- **Language**: {example['language'].title()}
- **Complexity**: {example['complexity']}
- **Description**: {example['description']}

```{example['language']}
{self._get_code_preview(example['path'])}
```

[📄 View full code]({example['path'].relative_to(self.project_root)})

---

"""
        
        examples_file = self.book_dir / "src" / "software" / "examples.md"
        examples_file.write_text(content)
    
    def _get_code_preview(self, file_path, max_lines=15):
        """Obtiene preview del código"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')[:max_lines]
            preview = '\n'.join(lines)
            if len(content.split('\n')) > max_lines:
                preview += '\n// ... (más código disponible)'
            return preview
        except:
            return "// Code preview not available"

def main():
    """Función principal"""
    project_root = os.getcwd()
    generator = DocumentationGenerator(project_root)
    
    print("🤖 Iniciando generación automática de documentación...")
    
    # Analizar proyecto
    analysis = generator.analyze_project()
    
    # Generar contenido
    generator.generate_markdown_content(analysis)
    
    # Guardar análisis para referencia
    analysis_file = generator.book_dir / "project_analysis.json"
    
    # Convertir paths a strings para serialización JSON
    def path_to_str(obj):
        if isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, list):
            return [path_to_str(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: path_to_str(value) for key, value in obj.items()}
        elif isinstance(obj, set):
            return list(obj)
        return obj
    
    clean_analysis = path_to_str(analysis)
    analysis_file.write_text(json.dumps(clean_analysis, indent=2))
    
    print(f"📋 Análisis guardado en: {analysis_file}")
    print("🎉 ¡Generación automática completada!")

if __name__ == "__main__":
    main()

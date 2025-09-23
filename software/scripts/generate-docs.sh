#!/bin/bash

# 🤖 Generador automático de documentación mdBook
# Este script analiza el proyecto y genera documentación automáticamente

set -e

# Get the project root (two levels up from scripts directory)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BOOK_DIR="$PROJECT_ROOT/software/book"
HARDWARE_DIR="$PROJECT_ROOT/hardware"
SOFTWARE_DIR="$PROJECT_ROOT/software"

echo "🚀 Generando documentación automáticamente..."
echo "📁 Project root: $PROJECT_ROOT"

# Función para crear estructura inicial de mdBook
setup_book_structure() {
    echo "📁 Creando estructura de mdBook..."
    
    # Crear directorios base
    mkdir -p "$BOOK_DIR/src"
    mkdir -p "$BOOK_DIR/src/hardware"
    mkdir -p "$BOOK_DIR/src/software" 
    mkdir -p "$BOOK_DIR/src/applications"
    mkdir -p "$BOOK_DIR/src/resources"
    
    # Crear book.toml si no existe
    if [ ! -f "$BOOK_DIR/book.toml" ]; then
        cat > "$BOOK_DIR/book.toml" << EOF
[book]
title = "UNIT Jun R3 Development Board"
authors = ["UNIT Electronics MX"]
description = "Complete documentation for UNIT Jun R3 Development Board"

[build]
build-dir = "book"

[output.html]
default-theme = "light"
preferred-dark-theme = "navy"
copy-fonts = true
mathjax-support = false
git-repository-url = "https://github.com/UNIT-Electronics-MX/unit_jun_r3_development_board"

[output.html.search]
enable = true
EOF
    fi
    
    # Crear introduction.md básico si no existe
    if [ ! -f "$BOOK_DIR/src/introduction.md" ]; then
        cat > "$BOOK_DIR/src/introduction.md" << EOF
# Introduction

Welcome to the UNIT Jun R3 Development Board documentation.

This interactive documentation provides everything you need to get started with your development board.

## What's Included

- 📋 **Hardware Documentation**: Complete specifications and schematics
- 💻 **Software Examples**: Ready-to-use code examples
- 🔧 **Development Guide**: Programming and setup instructions
- 🆘 **Support Resources**: Troubleshooting and help

*Documentation automatically generated on $(date '+%Y-%m-%d %H:%M:%S')*
EOF
    fi
    
    echo "✅ Estructura de mdBook creada"
}

# Función para generar página de hardware automáticamente
generate_hardware_docs() {
    echo "🔧 Generando documentación de hardware..."
    
    # Crear directorios necesarios
    mkdir -p "$BOOK_DIR/src/hardware"
    
    # Analizar archivos PDF y generar lista
    local schematic_files=$(find "$HARDWARE_DIR" -name "*.pdf" 2>/dev/null | head -5)
    local image_files=$(find "$HARDWARE_DIR" -name "*.png" -o -name "*.jpg" 2>/dev/null | head -10)
    
    # Generar overview automáticamente
    cat > "$BOOK_DIR/src/hardware/overview.md" << EOF
# Hardware Overview

> 📋 **Auto-generated**: $(date '+%Y-%m-%d %H:%M:%S')


## Available Resources

### Schematics
$(for file in $schematic_files; do
    filename=$(basename "$file")
    echo "- [$filename](../../../hardware/$filename)"
done)

### Board Images
$(for file in $image_files; do
    filename=$(basename "$file")
    if [[ $filename == *"top"* ]]; then
        echo "![Top View](../../../hardware/resources/$filename)"
    elif [[ $filename == *"bottom"* ]] || [[ $filename == *"btm"* ]]; then
        echo "![Bottom View](../../../hardware/resources/$filename)"
    elif [[ $filename == *"pinout"* ]]; then
        echo "![Pinout](../../../hardware/resources/$filename)"
    elif [[ $filename == *"dimension"* ]]; then
        echo "![Dimensions](../../../hardware/resources/$filename)"
    fi
done)

## Component Analysis

$(if [ -f "$HARDWARE_DIR/README.md" ]; then
    echo "### From Hardware README:"
    grep -E "^\|.*\|" "$HARDWARE_DIR/README.md" | head -10 || echo "No tables found"
fi)

EOF

    echo "✅ Hardware docs generados"
}

# Función para generar ejemplos de software automáticamente
generate_software_docs() {
    echo "💻 Generando documentación de software..."
    
    # Crear directorios necesarios
    mkdir -p "$BOOK_DIR/src/software"
    
    # Buscar ejemplos de código (incluyendo subdirectorios)
    local example_files=$(find "$SOFTWARE_DIR/examples" -type f \( -name "*.py" -o -name "*.cpp" -o -name "*.ino" -o -name "*.c" \) 2>/dev/null)
    
    echo "🔍 Archivos de ejemplo encontrados: $(echo "$example_files" | wc -l)"
    echo "📁 Buscando en: $SOFTWARE_DIR/examples"
    
    # Generar página de ejemplos
    cat > "$BOOK_DIR/src/software/examples.md" << EOF
# Code Examples

> 📋 **Auto-generated**: $(date '+%Y-%m-%d %H:%M:%S')

## Available Examples

$(if [ -z "$example_files" ]; then
    echo "⚠️ No example files found in $SOFTWARE_DIR/examples"
else
    for file in $example_files; do
        filename=$(basename "$file")
        dirname=$(basename "$(dirname "$file")")
        relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$file")
        ext="${filename##*.}"
        
        # Extract first comment lines as description
        description=$(head -10 "$file" | grep -E "^\s*(/\*|//|\*)" | head -3 | sed 's|^\s*\(/\*\|\*\*/\?\|//\)\s*||' | tr '\n' ' ')
        
        case $ext in
            py)
                echo "### 🐍 $dirname: $filename"
                if [ ! -z "$description" ]; then
                    echo "*$description*"
                    echo ""
                fi
                echo "\`\`\`python"
                head -25 "$file" | sed 's/^//' 
                echo "\`\`\`"
                echo "[📄 Ver código completo]($relative_path)"
                echo ""
                ;;
            cpp|ino|c)
                echo "### ⚡ $dirname: $filename"
                if [ ! -z "$description" ]; then
                    echo "*$description*"
                    echo ""
                fi
                echo "\`\`\`cpp"
                head -25 "$file" | sed 's/^//'
                echo "\`\`\`" 
                echo "[📄 Ver código completo]($relative_path)"
                echo ""
                ;;
        esac
    done
fi)

EOF

    echo "✅ Software docs generados"
}

# Función para generar especificaciones desde README
generate_specs_from_readme() {
    echo "📋 Generando especificaciones desde README..."
    
    if [ -f "$PROJECT_ROOT/README.md" ]; then
        # Extraer tabla de overview si existe
        local overview_table=$(sed -n '/| Feature/,/^$/p' "$PROJECT_ROOT/README.md")
        
        cat > "$BOOK_DIR/src/hardware/specifications.md" << EOF
# Hardware Specifications

> 📋 **Auto-generated from README.md**: $(date '+%Y-%m-%d %H:%M:%S')

## Feature Overview

$overview_table

## Additional Information

$(grep -A 10 -B 2 -i "specification\|feature\|characteristic" "$PROJECT_ROOT/README.md" | head -20)

EOF
    fi
}

# Función para actualizar SUMMARY.md automáticamente
update_summary() {
    echo "📑 Actualizando SUMMARY.md..."
    
    # Generar índice dinámicamente basado en archivos existentes
    cat > "$BOOK_DIR/src/SUMMARY.md" << 'EOF'
# Summary

[Introduction](./introduction.md)

# Hardware Documentation

- [Overview](./hardware/overview.md)
- [Pinout](./hardware/pinout.md) 
- [Specifications](./hardware/specifications.md)
- [Dimensions](./hardware/dimensions.md)
- [Schematic](./hardware/schematic.md)

# Software Documentation

- [Getting Started](./software/getting-started.md)
- [Examples](./software/examples.md)
  - [MicroPython](./software/examples/micropython.md)
  - [Arduino/C++](./software/examples/arduino.md)
- [API Reference](./software/api-reference.md)

# Applications

- [Use Cases](./applications/use-cases.md)
- [Integration Guide](./applications/integration.md)
- [Troubleshooting](./applications/troubleshooting.md)

# Resources

- [Downloads](./resources/downloads.md)
- [Support](./resources/support.md)
- [License](./resources/license.md)

---

*📅 Last updated: [DATE_PLACEHOLDER]*
EOF

    # Reemplazar placeholder con fecha actual
    sed -i "s/DATE_PLACEHOLDER/$(date '+%Y-%m-%d %H:%M:%S')/" "$BOOK_DIR/src/SUMMARY.md"
}

# Ejecutar generadores
setup_book_structure
generate_hardware_docs
generate_software_docs  
generate_specs_from_readme
update_summary

# Construir documentación
echo "🔨 Construyendo documentación..."
cd "$BOOK_DIR"
if mdbook build; then
    echo "✅ Documentación generada exitosamente!"
    echo "📁 Salida: $BOOK_DIR/book/"
    
    # Mostrar estadísticas
    echo ""
    echo "📊 Estadísticas:"
    echo "   - Páginas HTML: $(find book -name "*.html" | wc -l)"
    echo "   - Archivos fuente: $(find src -name "*.md" | wc -l)"
    echo "   - Imágenes: $(find ../../../hardware/resources -name "*.png" -o -name "*.jpg" | wc -l)"
else
    echo "❌ Error al generar documentación"
    exit 1
fi

echo ""
echo "🌐 Para ver la documentación:"
echo "   mdbook serve --open"
echo "   # o abrir: file://$BOOK_DIR/book/index.html"

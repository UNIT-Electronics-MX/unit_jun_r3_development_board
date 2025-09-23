#!/bin/bash

# 🤖 Generador automático de documentación mdBook
# Este script analiza el proyecto y genera documentación automáticamente

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOK_DIR="$PROJECT_ROOT/software/book"
HARDWARE_DIR="$PROJECT_ROOT/hardware"
SOFTWARE_DIR="$PROJECT_ROOT/software"

echo "🚀 Generando documentación automáticamente..."

# Función para generar página de hardware automáticamente
generate_hardware_docs() {
    echo "🔧 Generando documentación de hardware..."
    
    # Analizar archivos PDF y generar lista
    local schematic_files=$(find "$HARDWARE_DIR" -name "*.pdf" 2>/dev/null | head -5)
    local image_files=$(find "$HARDWARE_DIR" -name "*.png" -o -name "*.jpg" 2>/dev/null | head -10)
    
    # Generar overview automáticamente
    cat > "$BOOK_DIR/src/hardware/overview.md" << EOF
# Hardware Overview

> 📋 **Auto-generated**: $(date '+%Y-%m-%d %H:%M:%S')

The UNIT Touch Capacitive Sensor hardware documentation.

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
    
    # Buscar ejemplos de código
    local example_files=$(find "$SOFTWARE_DIR/examples" -name "*.py" -o -name "*.cpp" -o -name "*.ino" 2>/dev/null)
    
    # Generar página de ejemplos
    cat > "$BOOK_DIR/src/software/examples.md" << EOF
# Code Examples

> 📋 **Auto-generated**: $(date '+%Y-%m-%d %H:%M:%S')

## Available Examples

$(for file in $example_files; do
    filename=$(basename "$file")
    relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$file")
    ext="${filename##*.}"
    
    case $ext in
        py)
            echo "### 🐍 Python: $filename"
            echo "\`\`\`python"
            head -20 "$file" | sed 's/^//' 
            echo "\`\`\`"
            echo "[📄 Ver código completo]($relative_path)"
            echo ""
            ;;
        cpp|ino)
            echo "### ⚡ Arduino/C++: $filename"
            echo "\`\`\`cpp"
            head -20 "$file" | sed 's/^//'
            echo "\`\`\`" 
            echo "[📄 Ver código completo]($relative_path)"
            echo ""
            ;;
    esac
done)

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

#!/usr/bin/env bash
"""
Script de automatización final para generar documentación mdBook limpia
Sin duplicar títulos y manteniendo los templates originales intactos
"""

# Ejecutar el extractor inteligente
echo "🎯 Generando documentación limpia..."
python3 smart-extract-docs.py

# Construir el mdBook  
echo "🔨 Construyendo documentación..."
cd software/book && mdbook build

echo "✅ ¡Documentación lista!"
echo "📖 Para ver localmente: cd software/book && mdbook serve"
echo "🌐 Para desplegar: El workflow de GitHub Actions se encarga automáticamente"

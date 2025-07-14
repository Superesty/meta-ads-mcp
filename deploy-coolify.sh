#!/bin/bash

# Script de despliegue para Meta Ads MCP en Coolify
echo "🚀 Preparando despliegue de Meta Ads MCP para Coolify"

# Verificar que estamos en el directorio correcto
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto"
    exit 1
fi

echo "✅ Directorio del proyecto verificado"

# Crear .dockerignore si no existe
if [ ! -f ".dockerignore" ]; then
    echo "📝 Creando .dockerignore..."
    cat > .dockerignore << EOF
.git
.gitignore
.pytest_cache
.coverage
*.pyc
__pycache__
.venv
venv/
.env
*.log
tests/
examples/
.github/
start_with_token.bat
deploy-coolify.sh
coolify.env.example

# Exclude documentation files except README.md (required for build)
DEVELOPMENT.md
EJECUTAR_SERVIDOR.md
COOLIFY_DEPLOY.md
TRANSPORT_CONFIGURATIONS.md
SECURITY.md
COMMIT_SUMMARY.md
DOCKER_COMPOSE_INFO.md
*.md
!README.md
EOF
    echo "✅ .dockerignore creado"
fi

# Verificar Dockerfile
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile encontrado"
else
    echo "❌ Error: Dockerfile no encontrado"
    exit 1
fi

# Verificar docker-compose.yml
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml encontrado"
else
    echo "❌ Error: docker-compose.yml no encontrado"
    exit 1
fi

echo ""
echo "🎯 Preparación completa para Coolify"
echo ""
echo "📋 Pasos para desplegar en Coolify:"
echo ""
echo "1. 📂 Sube este repositorio a GitHub/GitLab"
echo ""
echo "2. 🌐 En Coolify, crea una nueva aplicación:"
echo "   - Tipo: Docker Compose"
echo "   - Repository: tu-repositorio"
echo "   - Branch: main"
echo ""
echo "3. ⚙️  Configura las variables de entorno en Coolify:"
echo "   META_ACCESS_TOKEN=tu_token_aqui"
echo "   MCP_LOG_LEVEL=INFO"
echo ""
echo "4. 🚀 Despliega la aplicación"
echo ""
echo "5. 🔗 Tu servidor estará disponible en:"
echo "   https://tu-dominio.com/mcp/"
echo ""
echo "📝 Para más detalles, consulta: coolify.env.example"

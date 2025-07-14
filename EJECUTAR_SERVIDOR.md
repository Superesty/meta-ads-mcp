# 🚀 Cómo Ejecutar el Servidor Meta Ads MCP

Este documento te guía paso a paso para poner en marcha el servidor MCP de Meta Ads en tu máquina local.

## ✅ Estado Actual

El servidor está **instalado y listo para usar**. Todos los archivos necesarios han sido creados:

- ✅ Paquete instalado en modo desarrollo
- ✅ Scripts de inicio y prueba creados  
- ✅ Problemas de Unicode en Windows corregidos
- ✅ Documentación de desarrollo añadida

## 🏃‍♂️ Inicio Rápido

### 1. Probar que Todo Funciona

```cmd
# Verificar la versión instalada
python -m meta_ads_mcp --version

# Debería mostrar: Meta Ads MCP v0.4.0
```

### 2. Ejecutar el Servidor

#### Opción A: Script de Inicio (Recomendado)
```cmd
# Iniciar con configuración automática
python start_server.py

# O para HTTP (desarrollo/pruebas)
python start_server.py --http --port 8080
```

#### Opción B: Comando Directo
```cmd
# Modo stdio (para clientes MCP como Claude/Cursor)
python -m meta_ads_mcp

# Modo HTTP (para desarrollo)
python -m meta_ads_mcp --transport streamable-http --port 8080
```

## 🔐 Configuración de Autenticación

### Método 1: Pipeboard (Más Fácil)

1. **Regístrate en [Pipeboard.co](https://pipeboard.co)**
2. **Genera un token API en [pipeboard.co/api-tokens](https://pipeboard.co/api-tokens)**
3. **Configura la variable de entorno:**

```cmd
# En Windows (Command Prompt)
set PIPEBOARD_API_TOKEN=tu_token_aqui

# En Windows (PowerShell)
$env:PIPEBOARD_API_TOKEN="tu_token_aqui"

# Para hacerlo permanente, añádelo a las variables de entorno del sistema
```

### Método 2: App de Meta Custom (Avanzado)

1. **Crea una app en [Meta for Developers](https://developers.facebook.com/)**
2. **Añade el producto "Marketing API"**
3. **Configura las variables:**

```cmd
# En Windows
set META_APP_ID=tu_app_id
set META_APP_SECRET=tu_app_secret
```

## 🧪 Probar la Configuración

### Prueba de Autenticación
```cmd
# Prueba básica
python test_meta_ads_auth.py

# Con App ID específico  
python test_meta_ads_auth.py --app-id TU_APP_ID

# Forzar nuevo login
python test_meta_ads_auth.py --app-id TU_APP_ID --force-login
```

### Prueba del Servidor HTTP
```cmd
# Iniciar servidor HTTP de prueba
python start_server.py --http --port 8080

# En otra terminal, probar que responde
curl http://localhost:8080/mcp/streamable-http/
```

## 📋 Comandos Útiles

```cmd
# Ver todas las opciones
python -m meta_ads_mcp --help

# Solo hacer login (sin iniciar servidor)
python -m meta_ads_mcp --login

# Iniciar con logs detallados
set MCP_LOG_LEVEL=DEBUG
python -m meta_ads_mcp --transport streamable-http --port 8080

# Probar autenticación
python test_meta_ads_auth.py --help
```

## 🔧 Configuración para Clientes MCP

### Claude Desktop
Añade a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "python",
      "args": ["-m", "meta_ads_mcp"],
      "cwd": "d:\\vsc\\mcps\\meta-ads-mcp"
    }
  }
}
```

### Cursor
Añade a tu `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "python",
      "args": ["-m", "meta_ads_mcp"],
      "cwd": "d:\\vsc\\mcps\\meta-ads-mcp"
    }
  }
}
```

## 🆘 Solución de Problemas

### Problema: "meta_ads_mcp not found"
```cmd
# Reinstalar en modo desarrollo
pip install -e .
```

### Problema: Puerto ocupado
```cmd
# Usar puerto diferente
python -m meta_ads_mcp --transport streamable-http --port 8081
```

### Problema: Error de autenticación
```cmd
# Limpiar cache de tokens (Windows)
rmdir /s %APPDATA%\\meta-ads-mcp
```

### Problema: Caracteres Unicode
Los caracteres emoji han sido removidos para compatibilidad con Windows. Si ves errores de encoding, asegúrate de estar usando Command Prompt o PowerShell actualizado.

## 📁 Archivos Importantes

- `start_server.py` - Script de inicio rápido
- `test_meta_ads_auth.py` - Prueba de autenticación  
- `DEVELOPMENT.md` - Guía completa de desarrollo
- `meta_ads_mcp/core/server.py` - Servidor principal
- `pyproject.toml` - Configuración del proyecto

## 📞 Soporte

- **Documentación completa**: [README.md](README.md)
- **Instalación local**: [LOCAL_INSTALLATION.md](LOCAL_INSTALLATION.md)  
- **Desarrollo**: [DEVELOPMENT.md](DEVELOPMENT.md)
- **Discord**: [https://discord.gg/hNxpJcqM52](https://discord.gg/hNxpJcqM52)
- **Email**: info@pipeboard.co

## ✨ Siguiente Paso

Una vez que tengas el servidor funcionando:

1. **Configura tu autenticación** (Pipeboard o Meta App)
2. **Prueba con**: `python test_meta_ads_auth.py`
3. **Inicia el servidor**: `python start_server.py`
4. **Conecta tu cliente MCP** (Claude, Cursor, etc.)

¡Tu servidor Meta Ads MCP está listo para usar! 🎉

# Configuraciones de Transporte - Meta Ads MCP Server

## Resumen de Transportes Soportados

El servidor Meta Ads MCP soporta 2 tipos de transporte principales:

1. **STDIO** - Para clientes MCP (Claude Desktop, Cursor, etc.)
2. **Streamable HTTP** - Para acceso web/API REST

## 1. Transporte STDIO (Default)

### Características
- **Comunicación**: Proceso-a-proceso vía stdin/stdout
- **Uso Principal**: Clientes MCP nativos
- **Estado**: Stateful (mantiene sesión)
- **Puerto**: No requiere puerto (comunicación directa)

### Comandos de Inicio

```bash
# Modo básico (stdio predeterminado)
python -m meta_ads_mcp

# Modo explícito stdio
python -m meta_ads_mcp --transport stdio

# Con script helper
python start_server.py

# Con batch (Windows + token directo)
start_with_token.bat
```

### Configuración para Claude Desktop

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "python",
      "args": ["-m", "meta_ads_mcp"],
      "env": {
        "META_ACCESS_TOKEN": "tu_token_aqui"
      }
    }
  }
}
```

### Configuración para Cursor

```json
{
  "mcp": {
    "servers": {
      "meta-ads": {
        "command": "python",
        "args": ["-m", "meta_ads_mcp"],
        "env": {
          "META_ACCESS_TOKEN": "tu_token_aqui"
        }
      }
    }
  }
}
```

## 2. Transporte Streamable HTTP

### Características
- **Comunicación**: HTTP REST API
- **Uso Principal**: Desarrollo, testing, VPS deployment
- **Estado**: Stateless (sin sesión persistente)
- **Puerto**: Configurable (default: 8080)
- **Formatos**: JSON (default) o SSE

### Comandos de Inicio

```bash
# HTTP básico (puerto 8080)
python -m meta_ads_mcp --transport streamable-http

# HTTP con puerto personalizado
python -m meta_ads_mcp --transport streamable-http --port 3000

# HTTP con host personalizado
python -m meta_ads_mcp --transport streamable-http --host 0.0.0.0 --port 8080

# HTTP con formato SSE
python -m meta_ads_mcp --transport streamable-http --sse-response

# Con script helper
python start_server.py --http --port 8080

# Desarrollo local completo
python start_server.py --http --host 0.0.0.0 --port 8080
```

### Endpoints Disponibles

```bash
# Endpoint principal MCP
http://localhost:8080/mcp/

# Health check
http://localhost:8080/mcp/health

# Test de conectividad
curl http://localhost:8080/mcp/
```

### Autenticación HTTP

#### Método 1: Bearer Token (Recomendado)
```bash
curl -X POST http://localhost:8080/mcp/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

#### Método 2: Header Personalizado
```bash
curl -X POST http://localhost:8080/mcp/ \
  -H "X-META-ACCESS-TOKEN: TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

#### Método 3: Meta App OAuth (Avanzado)
```bash
curl -X POST http://localhost:8080/mcp/ \
  -H "X-META-APP-ID: TU_APP_ID_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

## 3. Configuraciones de Despliegue

### Desarrollo Local

```bash
# STDIO para testing con Claude Desktop
python start_server.py

# HTTP para testing web
python start_server.py --http --port 8080
```

### Producción VPS (Docker)

#### Variables de Entorno
```env
# En .env o coolify.env
META_ACCESS_TOKEN=tu_token_real
MCP_LOG_LEVEL=INFO
```

#### Docker Compose
```yaml
version: '3.8'
services:
  meta-ads-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - META_ACCESS_TOKEN=${META_ACCESS_TOKEN}
      - MCP_LOG_LEVEL=${MCP_LOG_LEVEL:-INFO}
    command: python -m meta_ads_mcp --transport streamable-http --host 0.0.0.0 --port 8080
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/mcp/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### Coolify Deployment
```bash
# Comando del contenedor en Coolify
python -m meta_ads_mcp --transport streamable-http --host 0.0.0.0 --port 8080

# Variables de entorno en Coolify
META_ACCESS_TOKEN=tu_token_real
MCP_LOG_LEVEL=INFO
```

## 4. Configuraciones de Cliente

### Para STDIO (Local)

#### Claude Desktop (`~/.claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "python",
      "args": ["-m", "meta_ads_mcp"],
      "env": {
        "META_ACCESS_TOKEN": "tu_token_local"
      }
    }
  }
}
```

### Para HTTP (Remoto)

#### Claude Desktop con HTTP
```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "https://tu-dominio.com/mcp/",
        "-H", "Authorization: Bearer tu_token_produccion",
        "-H", "Content-Type: application/json",
        "-d", "@-"
      ]
    }
  }
}
```

#### Cursor con HTTP
```json
{
  "mcp": {
    "servers": {
      "meta-ads": {
        "url": "https://tu-dominio.com/mcp/",
        "headers": {
          "Authorization": "Bearer tu_token_produccion"
        }
      }
    }
  }
}
```

## 5. Troubleshooting por Transporte

### STDIO Issues
```bash
# Verificar que el comando funciona
python -m meta_ads_mcp --version

# Test rápido de autenticación
python test_meta_ads_auth.py

# Logs del cliente MCP
# Claude Desktop: Ver logs en la aplicación
# Cursor: Ver terminal output
```

### HTTP Issues
```bash
# Verificar que el servidor está corriendo
curl http://localhost:8080/mcp/

# Test de autenticación
curl -X POST http://localhost:8080/mcp/ \
  -H "Authorization: Bearer tu_token" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'

# Verificar logs del servidor
python -m meta_ads_mcp --transport streamable-http --port 8080
```

## 6. Comparación de Transportes

| Característica | STDIO | Streamable HTTP |
|----------------|-------|-----------------|
| **Uso Principal** | Clientes MCP | Web/API/VPS |
| **Estado** | Stateful | Stateless |
| **Puerto** | No requiere | 8080 (configurable) |
| **Autenticación** | Env vars | Headers HTTP |
| **Desarrollo** | ✅ Fácil local | ✅ Fácil testing |
| **Producción** | ❌ Solo local | ✅ VPS/Cloud |
| **Debugging** | Medio | ✅ Fácil (curl) |
| **Escalabilidad** | ❌ Proceso único | ✅ Load balancer |

## 7. Recomendaciones

### Para Desarrollo Local
```bash
# STDIO para integración con Claude Desktop/Cursor
python start_server.py

# HTTP para testing manual
python start_server.py --http --port 8080
```

### Para Producción VPS
```bash
# Siempre HTTP con host 0.0.0.0
python -m meta_ads_mcp --transport streamable-http --host 0.0.0.0 --port 8080
```

### Para Testing
```bash
# Local testing
python test_meta_ads_auth.py

# HTTP testing
curl http://localhost:8080/mcp/
```

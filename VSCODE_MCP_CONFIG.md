# 🔧 Configuración MCP Server para VS Code - Post VPS Deploy

## 📋 Configuraciones Disponibles

Después del despliegue en VPS, tienes **3 opciones** para conectar VS Code al MCP server:

### 1️⃣ **Opción 1: Servidor Local (Desarrollo)**
Para desarrollo y testing local:

#### VS Code Settings (settings.json)
```json
{
  "mcp.servers": {
    "meta-ads-local": {
      "command": "python",
      "args": ["-m", "meta_ads_mcp"],
      "env": {
        "META_ACCESS_TOKEN": "TU_TOKEN_AQUI"
      }
    }
  }
}
```

#### Claude Desktop Local
```json
{
  "mcpServers": {
    "meta-ads-local": {
      "command": "python",
      "args": ["-m", "meta_ads_mcp"],
      "env": {
        "META_ACCESS_TOKEN": "TU_TOKEN_AQUI"
      }
    }
  }
}
```

---

### 2️⃣ **Opción 2: VPS con Puerto Directo**
Conexión directa al puerto 3001 del VPS:

#### VS Code Settings (settings.json)
```json
{
  "mcp.servers": {
    "meta-ads-vps": {
      "transport": "http",
      "url": "http://TU-IP-VPS:3001/mcp/",
      "headers": {
        "X-META-ACCESS-TOKEN": "TU_TOKEN_AQUI",
        "Content-Type": "application/json"
      }
    }
  }
}
```

#### Claude Desktop VPS (Puerto Directo)
```json
{
  "mcpServers": {
    "meta-ads-vps": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "http://TU-IP-VPS:3001/mcp/",
        "-H", "X-META-ACCESS-TOKEN: TU_TOKEN_AQUI",
        "-H", "Content-Type: application/json",
        "-d", "@-"
      ]
    }
  }
}
```

---

### 3️⃣ **Opción 3: VPS con Dominio (Recomendado)**
Conexión via dominio con HTTPS (configuración final de producción):

#### VS Code Settings (settings.json)
```json
{
  "mcp.servers": {
    "meta-ads-production": {
      "transport": "http",
      "url": "https://TU-DOMINIO.com/mcp/",
      "headers": {
        "X-META-ACCESS-TOKEN": "TU_TOKEN_AQUI",
        "Content-Type": "application/json"
      }
    }
  }
}
```

#### Claude Desktop Producción
```json
{
  "mcpServers": {
    "meta-ads-production": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "https://TU-DOMINIO.com/mcp/",
        "-H", "X-META-ACCESS-TOKEN: TU_TOKEN_AQUI",
        "-H", "Content-Type: application/json",
        "-d", "@-"
      ]
    }
  }
}
```

---

## 🔗 **URLs de Conexión Actuales**

### Según el Estado de tu Despliegue:

#### Si Aún No Tienes Dominio Configurado:
```bash
# Testing directo por IP y puerto
http://TU-IP-VPS:3001/mcp/

# Ejemplo (reemplaza con tu IP real):
http://147.93.67.123:3001/mcp/
```

#### Cuando Configures el Dominio en Coolify:
```bash
# URL final de producción
https://mcp.cogitia.com.es/mcp/
https://meta-ads.cogitia.com.es/mcp/
https://api.cogitia.com.es/mcp/
```

---

## ⚙️ **Configuración Paso a Paso en VS Code**

### 1. **Abrir VS Code Settings**
```
Ctrl+Shift+P → "Preferences: Open Settings (JSON)"
```

### 2. **Agregar Configuración MCP**
```json
{
  // ...otras configuraciones...
  
  "mcp.servers": {
    "meta-ads": {
      "transport": "http",
      "url": "https://TU-DOMINIO.com/mcp/",
      "headers": {
        "X-META-ACCESS-TOKEN": "TU_TOKEN_REAL_AQUI",
        "Content-Type": "application/json"
      }
    }
  }
}
```

### 3. **Recargar VS Code**
```
Ctrl+Shift+P → "Developer: Reload Window"
```

---

## 🧪 **Testing de Conectividad**

### Verificar que el Servidor Responde:
```bash
# Test básico
curl http://TU-IP-VPS:3001/mcp/

# Test con autenticación
curl -X POST http://TU-IP-VPS:3001/mcp/ \
  -H "X-META-ACCESS-TOKEN: TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

### Respuesta Esperada:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "mcp_meta_ads_get_campaigns",
        "description": "Get campaigns from Meta Ads API"
      },
      // ... más herramientas (24 total)
    ]
  },
  "id": 1
}
```

---

## 🔧 **Variables que Necesitas Reemplazar**

### En las Configuraciones:
```bash
TU-IP-VPS          → IP real de tu VPS (ej: 147.93.67.123)
TU-DOMINIO.com     → Tu dominio configurado en Coolify
TU_TOKEN_AQUI      → Tu access token real de Meta
```

### Ejemplo con Datos Reales:
```json
{
  "mcp.servers": {
    "meta-ads": {
      "transport": "http",
      "url": "https://mcp.cogitia.com.es/mcp/",
      "headers": {
        "X-META-ACCESS-TOKEN": "EAAPOtPtxZBMs...",
        "Content-Type": "application/json"
      }
    }
  }
}
```

---

## 📁 **Ubicación de Archivos de Configuración**

### VS Code:
```bash
# Windows
%APPDATA%\Code\User\settings.json

# macOS
~/Library/Application Support/Code/User/settings.json

# Linux
~/.config/Code/User/settings.json
```

### Claude Desktop:
```bash
# Windows
%APPDATA%\Claude\claude_desktop_config.json

# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Linux
~/.config/claude/claude_desktop_config.json
```

---

## 🚨 **Troubleshooting**

### Si VS Code No Conecta:
1. **Verificar URL**: Asegúrate que el servidor responde
2. **Verificar Token**: Confirma que el access token es válido
3. **Verificar Headers**: Content-Type debe ser application/json
4. **Verificar Firewall**: Puerto 3001 debe estar abierto

### Si Aparece Error de CORS:
Agrega estos headers:
```json
"headers": {
  "X-META-ACCESS-TOKEN": "TU_TOKEN",
  "Content-Type": "application/json",
  "Origin": "vscode://",
  "User-Agent": "VSCode-MCP-Client"
}
```

---

## 🎯 **Recomendación Final**

### Para Desarrollo:
**Usa Opción 1** (servidor local) - más rápido y fácil de debuggear

### Para Producción:
**Usa Opción 3** (dominio HTTPS) - más seguro y profesional

### Para Testing:
**Usa Opción 2** (IP:puerto) - para verificar que el VPS funciona

---

**¿Tienes ya la IP de tu VPS y el token? Te ayudo a crear la configuración exacta para tu caso.**

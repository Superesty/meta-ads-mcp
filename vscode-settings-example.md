# VS Code MCP Configuration - Meta Ads Server

## 📋 Configuración Rápida para VS Code

### 🚀 **Opción 1: VPS con Puerto Directo (Inmediato)**
Copia esto en tu `settings.json` de VS Code:

```json
{
  "mcp.servers": {
    "meta-ads-vps": {
      "transport": "http", 
      "url": "http://TU-IP-VPS:3001/mcp/",
      "headers": {
        "X-META-ACCESS-TOKEN": "TU_TOKEN_REAL_AQUI",
        "Content-Type": "application/json"
      }
    }
  }
}
```

### 🌐 **Opción 2: VPS con Dominio (Producción)**
Cuando configures el dominio en Coolify:

```json
{
  "mcp.servers": {
    "meta-ads-production": {
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

### 🏠 **Opción 3: Servidor Local (Desarrollo)**
Para desarrollo local:

```json
{
  "mcp.servers": {
    "meta-ads-local": {
      "command": "python",
      "args": ["-m", "meta_ads_mcp"],
      "env": {
        "META_ACCESS_TOKEN": "TU_TOKEN_REAL_AQUI"
      }
    }
  }
}
```

---

## 🔧 **Cómo Aplicar la Configuración**

### 1. **Abrir Settings de VS Code**
```
Ctrl+Shift+P → "Preferences: Open Settings (JSON)"
```

### 2. **Agregar la Configuración**
Pega una de las configuraciones de arriba dentro de las llaves `{}`

### 3. **Reemplazar Variables**
- `TU-IP-VPS` → IP real de tu VPS
- `TU-DOMINIO.com` → Tu dominio configurado
- `TU_TOKEN_REAL_AQUI` → Tu access token de Meta

### 4. **Reiniciar VS Code**
```
Ctrl+Shift+P → "Developer: Reload Window"
```

---

## 🧪 **Testing de la Conexión**

### Verificar que VS Code Conecta:
1. Abre la **Command Palette** (`Ctrl+Shift+P`)
2. Busca comandos que empiecen con "MCP" o "Meta Ads"
3. Deberías ver las 24 herramientas disponibles

### Testing Manual:
```bash
# Verificar que el servidor responde
curl http://TU-IP-VPS:3001/mcp/

# Test con token
curl -X POST http://TU-IP-VPS:3001/mcp/ \
  -H "X-META-ACCESS-TOKEN: TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

---

## 📁 **Ubicación del Archivo Settings**

### Windows:
```
%APPDATA%\Code\User\settings.json
```

### macOS:
```
~/Library/Application Support/Code/User/settings.json
```

### Linux:
```
~/.config/Code/User/settings.json
```

---

## 🚨 **Troubleshooting**

### Si No Aparecen los Comandos MCP:
1. **Verificar extensión MCP**: Instala la extensión oficial de MCP
2. **Verificar sintaxis JSON**: El archivo settings.json debe tener JSON válido
3. **Verificar URL**: Confirma que el servidor responde en la URL configurada
4. **Verificar token**: Asegúrate que el access token sea válido

### Errores Comunes:
```json
// ❌ INCORRECTO - falta Content-Type
"headers": {
  "X-META-ACCESS-TOKEN": "token"
}

// ✅ CORRECTO - incluye Content-Type
"headers": {
  "X-META-ACCESS-TOKEN": "token",
  "Content-Type": "application/json"
}
```

---

## 🎯 **Configuración Recomendada por Caso**

### 👨‍💻 **Para Desarrollo:**
**Usa Opción 3** (local) - Más rápido y fácil de debuggear

### 🧪 **Para Testing VPS:**
**Usa Opción 1** (IP:puerto) - Verifica que el VPS funciona

### 🚀 **Para Producción:**
**Usa Opción 2** (dominio HTTPS) - Más seguro y profesional

---

**¿Necesitas ayuda con algún paso específico o tienes ya los datos del VPS para crear la configuración exacta?**

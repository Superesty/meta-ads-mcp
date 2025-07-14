# 🔧 Port Configuration Fix - Coolify

## ❌ **Problema**
```
Bind for 0.0.0.0:8080 failed: port is already allocated
```

## 🔍 **Causa**
El puerto 8080 ya está siendo usado por otro servicio en tu servidor VPS.

## ✅ **Solución Implementada**

### Cambio de Puerto
```yaml
# ANTES
ports:
  - "8080:8080"  # ❌ Puerto 8080 ocupado

# DESPUÉS  
ports:
  - "3001:8080"  # ✅ Puerto 3001 libre (mapeado a 8080 interno)
```

### Configuración Actual
- **Puerto Externo**: 3001 (accesible desde internet)
- **Puerto Interno**: 8080 (dentro del container)
- **Mapeo**: `host:3001 → container:8080`

## 🌐 **URLs de Acceso**

### Desarrollo/Testing Directo
```bash
# Acceso directo por puerto
http://tu-servidor.com:3001/mcp/
```

### Producción con Dominio (Recomendado)
```bash
# Coolify maneja el proxy automáticamente
https://tu-dominio.com/mcp/
```

## 🔄 **Puertos Alternativos**

Si el puerto 3001 también está ocupado, puedes usar:

### Opciones Comunes Disponibles
```yaml
# Opción 1: Puerto 3002
ports:
  - "3002:8080"

# Opción 2: Puerto 8081  
ports:
  - "8081:8080"

# Opción 3: Puerto 9001
ports:
  - "9001:8080"

# Opción 4: Puerto 8888
ports:
  - "8888:8080"
```

### Verificar Puertos Disponibles en tu VPS
```bash
# Verificar qué puertos están en uso
sudo netstat -tulpn | grep :8080
sudo netstat -tulpn | grep :3001
sudo netstat -tulpn | grep :3002

# O con ss (más moderno)
ss -tulpn | grep :8080
ss -tulpn | grep :3001
```

## 📋 **Servicios Comunes que Usan Puerto 8080**

| Servicio | Puerto Típico | Conflicto |
|----------|---------------|-----------|
| **Jenkins** | 8080 | ✅ Muy común |
| **Tomcat** | 8080 | ✅ Frecuente |
| **Nginx Proxy** | 8080 | ✅ Posible |
| **Development Servers** | 8080 | ✅ Habitual |
| **HTTP Alt** | 8080 | ✅ Estándar |

## 🚀 **Próximos Pasos**

### 1. **Redeploy con Puerto 3001**
El cambio ya está commiteado. Ve a Coolify y redespliega.

### 2. **Si Puerto 3001 También Falla**
Edita `docker-compose.yaml` en Coolify:
```yaml
ports:
  - "TU_PUERTO_LIBRE:8080"
```

### 3. **Configuración de Dominio**
Una vez funcionando:
- Configura tu dominio en Coolify
- Habilita HTTPS
- El proxy manejará el enrutamiento automáticamente

## ✅ **Testing Post-Deploy**

```bash
# Test de conectividad directa
curl http://tu-servidor.com:3001/mcp/

# Test con dominio (después de configurar)
curl https://tu-dominio.com/mcp/

# Test completo con autenticación
curl -X POST https://tu-dominio.com/mcp/ \
  -H "X-META-ACCESS-TOKEN: tu_token" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

## 📝 **Notas Importantes**

### Para Clientes MCP
```json
// Configuración final para producción
{
  "mcpServers": {
    "meta-ads": {
      "url": "https://tu-dominio.com/mcp/",
      "headers": {
        "X-META-ACCESS-TOKEN": "tu_token"
      }
    }
  }
}
```

### Puerto vs Dominio
- **Puerto directo**: Para testing y debugging
- **Dominio**: Para producción y clientes MCP
- **HTTPS**: Siempre recomendado para producción

---

**Estado**: ✅ **LISTO PARA REDEPLOY CON PUERTO 3001**

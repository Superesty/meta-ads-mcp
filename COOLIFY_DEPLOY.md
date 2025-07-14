# 🚀 Guía de Despliegue en Coolify - Meta Ads MCP

## 📋 Preparación

### 1. Repositorio en Git
Primero, asegúrate de que tu código esté en un repositorio Git (GitHub, GitLab, etc.):

```bash
git add .
git commit -m "Preparar para despliegue en Coolify"
git push origin main
```

## 🔧 Configuración en Coolify

### 1. Crear Nueva Aplicación
1. **Accede a tu panel de Coolify**
2. **Crea una nueva aplicación**:
   - Tipo: **Docker Compose**
   - Source: Tu repositorio Git
   - Branch: `main`

### 📁 Archivos Docker Compose
**Importante**: El repositorio incluye ambos archivos para máxima compatibilidad:
- `docker-compose.yml` (extensión estándar)
- `docker-compose.yaml` (extensión alternativa)

Coolify automáticamente detectará el archivo correcto según su configuración.

### 2. Variables de Entorno
En Coolify, configura estas variables de entorno:

#### Variables Requeridas:
```env
META_ACCESS_TOKEN=TU_TOKEN_REAL_AQUI
```

#### Variables Opcionales:
```env
MCP_LOG_LEVEL=INFO
```

### 3. Configuración de Red
- **Puerto interno**: 8080
- **Dominio**: Configura tu dominio o subdominio
- **HTTPS**: Habilitar (recomendado)

### 4. Healthcheck
Coolify detectará automáticamente el healthcheck configurado en:
```
GET /mcp/
```

## 🌐 URL del Servidor

Una vez desplegado, tu servidor estará disponible en:
```
https://tu-dominio.com/mcp/
```

## 🔗 Configuración de Clientes MCP

### Para Claude Desktop:
```json
{
  "mcpServers": {
    "meta-ads": {
      "url": "https://tu-dominio.com/mcp/",
      "headers": {
        "X-META-ACCESS-TOKEN": "TU_TOKEN_REAL_AQUI"
      }
    }
  }
}
```

### Para Cursor:
```json
{
  "mcpServers": {
    "meta-ads": {
      "url": "https://tu-dominio.com/mcp/"
    }
  }
}
```

## 🧪 Probar el Despliegue

### Test Básico:
```bash
curl https://tu-dominio.com/mcp/
```

### Test con Herramientas:
```bash
curl -X POST https://tu-dominio.com/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "X-META-ACCESS-TOKEN: tu_token" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## 📊 Monitoreo

Coolify proporcionará:
- **Logs en tiempo real**
- **Métricas de recursos**
- **Status del healthcheck**
- **Reinicio automático** si el servicio falla

## 🔒 Seguridad

### Variables de Entorno:
- ✅ **META_ACCESS_TOKEN**: Almacenado de forma segura en Coolify
- ✅ **HTTPS**: Habilitado automáticamente
- ✅ **Isolation**: Contenedor aislado

### Recomendaciones:
1. **Usa dominios específicos**: `meta-ads-mcp.tu-dominio.com`
2. **Configura headers de seguridad** en tu proxy reverso
3. **Monitorea los logs** regularmente
4. **Rota el access token** periódicamente

## 🔧 Troubleshooting

### Problema: Container no inicia
```bash
# Verificar logs en Coolify
# Comprobar variables de entorno
# Verificar puerto 8080 disponible
```

### Problema: API no responde
```bash
# Verificar META_ACCESS_TOKEN válido
# Comprobar conectividad con Meta API
# Revisar logs de la aplicación
```

### Problema: Clientes MCP no conectan
```bash
# Verificar URL correcta: https://tu-dominio.com/mcp/
# Comprobar headers de autenticación
# Verificar CORS si es necesario
```

## 🎯 Resultado Final

Tendrás:
- ✅ **Servidor MCP ejecutándose 24/7**
- ✅ **URL pública accesible**
- ✅ **Monitoreo automático**
- ✅ **Reinicio automático**
- ✅ **HTTPS configurado**
- ✅ **Logs centralizados**

¡Tu Meta Ads MCP estará listo para usar desde cualquier cliente MCP en internet! 🚀

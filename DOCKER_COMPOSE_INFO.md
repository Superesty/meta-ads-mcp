# Docker Compose Files - Compatibilidad

## 📁 Archivos Disponibles

Este proyecto incluye **dos archivos Docker Compose idénticos**:

- `docker-compose.yml` (extensión `.yml`)
- `docker-compose.yaml` (extensión `.yaml`)

## 🤔 ¿Por Qué Dos Archivos?

### Compatibilidad con Plataformas
Diferentes plataformas de despliegue esperan diferentes extensiones:

| Plataforma | Extensión Esperada | Notas |
|------------|-------------------|-------|
| **Coolify** | `.yaml` | Algunas versiones buscan específicamente `.yaml` |
| **Docker CLI** | `.yml` o `.yaml` | Acepta ambas |
| **Portainer** | `.yml` | Prefiere `.yml` |
| **Rancher** | `.yaml` | Prefiere `.yaml` |
| **GitHub Actions** | `.yml` | Convención estándar |

### Error Típico en Coolify
```
Docker Compose file not found at: /docker-compose.yaml
Check if you used the right extension (.yaml or .yml) in the compose file name.
```

## ✅ Solución Implementada

### Archivos Sincronizados
Ambos archivos contienen exactamente la misma configuración:

```yaml
version: '3.8'

services:
  meta-ads-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - META_ACCESS_TOKEN=${META_ACCESS_TOKEN}
      - PIPEBOARD_API_TOKEN=${PIPEBOARD_API_TOKEN:-}
      - META_APP_ID=${META_APP_ID:-}
      - META_APP_SECRET=${META_APP_SECRET:-}
      - MCP_LOG_LEVEL=${MCP_LOG_LEVEL:-INFO}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/mcp/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Mantenimiento
Si necesitas modificar la configuración Docker Compose:

1. **Edita ambos archivos** para mantener la sincronización
2. **O usa este comando** para sincronizar automáticamente:
   ```bash
   cp docker-compose.yml docker-compose.yaml
   ```

## 🚀 Uso por Plataforma

### Coolify
- Detecta automáticamente `docker-compose.yaml`
- Si no encuentra `.yaml`, busca `.yml`
- ✅ **Funciona con ambos archivos**

### Docker CLI Local
```bash
# Cualquiera de estos comandos funciona:
docker-compose up -d
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yaml up -d
```

### Docker Compose V2
```bash
# Cualquiera de estos comandos funciona:
docker compose up -d
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yaml up -d
```

## 📋 Verificación

Para verificar que ambos archivos están sincronizados:

```bash
# En Windows
fc docker-compose.yml docker-compose.yaml

# En Linux/Mac
diff docker-compose.yml docker-compose.yaml
```

**Resultado esperado**: Sin diferencias (archivos idénticos)

## 🔄 Actualización Automática

Si necesitas un script para mantener ambos archivos sincronizados:

### Windows (PowerShell)
```powershell
Copy-Item docker-compose.yml docker-compose.yaml -Force
Write-Host "Archivos Docker Compose sincronizados"
```

### Linux/Mac (Bash)
```bash
cp docker-compose.yml docker-compose.yaml
echo "Archivos Docker Compose sincronizados"
```

## 🎯 Resultado

Con esta configuración:
- ✅ **Coolify**: Encuentra `docker-compose.yaml`
- ✅ **Docker CLI**: Funciona con cualquier extensión
- ✅ **Compatibilidad**: Universal con todas las plataformas
- ✅ **Mantenimiento**: Fácil sincronización cuando sea necesario

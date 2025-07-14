# Guía de Desarrollo - Meta Ads MCP Server

Esta guía te ayudará a poner en marcha el servidor MCP de Meta Ads para desarrollo local.

## 🚀 Inicio Rápido

### 1. Instalación de Dependencias

```bash
# Instalar en modo desarrollo
pip install -e .

# O usar uv (recomendado)
uv pip install -e .
```

### 2. Configuración de Autenticación

Tienes dos opciones de autenticación:

#### Opción A: Pipeboard (Recomendado - Más Fácil)
```bash
# Obtén tu token en https://pipeboard.co/api-tokens
export PIPEBOARD_API_TOKEN=tu_token_aqui
```

#### Opción B: App de Meta Custom (Avanzado)
```bash
# Crea una app en https://developers.facebook.com/
export META_APP_ID=tu_app_id
export META_APP_SECRET=tu_app_secret  # Opcional
```

### 3. Prueba de Autenticación

```bash
# Prueba básica
python test_meta_ads_auth.py

# Con App ID específico
python test_meta_ads_auth.py --app-id TU_APP_ID

# Forzar nuevo login
python test_meta_ads_auth.py --app-id TU_APP_ID --force-login
```

### 4. Ejecutar el Servidor

```bash
# Método 1: Script de inicio rápido
python start_server.py

# Método 2: Comando directo
python -m meta_ads_mcp

# Método 3: Con argumentos específicos
python -m meta_ads_mcp --app-id TU_APP_ID
```

## 🌐 Modos de Transporte

### Modo stdio (Para clientes MCP como Claude/Cursor)
```bash
python -m meta_ads_mcp
```

### Modo HTTP (Para desarrollo/pruebas)
```bash
# Servidor HTTP en puerto 8080
python -m meta_ads_mcp --transport streamable-http --port 8080

# O usando el script de inicio
python start_server.py --http --port 8080
```

## 🔐 Flujo de Autenticación

### Con Pipeboard
1. El servidor detecta `PIPEBOARD_API_TOKEN`
2. Si no hay token cached, abre el navegador automáticamente
3. Completas la autorización en pipeboard.co
4. El token se guarda automáticamente

### Con Meta App Custom
1. El servidor detecta `META_APP_ID`
2. Inicia servidor de callback local en puerto 8888
3. Abre navegador para OAuth de Meta
4. Autoriza la aplicación
5. Token se guarda en cache local

## 🧪 Pruebas

### Ejecutar Tests
```bash
# Tests básicos
pytest tests/

# Tests específicos
pytest tests/test_duplication.py
pytest tests/test_http_transport.py
```

### Verificar Servidor
```bash
# Verificar que el servidor responde
curl http://localhost:8080/mcp/streamable-http/

# Probar herramienta específica (requiere autenticación)
curl -X POST http://localhost:8080/mcp/streamable-http/ \
  -H "Authorization: Bearer tu_token" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"mcp_meta_ads_get_ad_accounts","arguments":{}}}'
```

## 📁 Estructura del Proyecto

```
meta_ads_mcp/
├── core/
│   ├── server.py          # Servidor principal MCP
│   ├── auth.py            # Autenticación Meta OAuth
│   ├── pipeboard_auth.py  # Autenticación Pipeboard  
│   ├── api.py             # Cliente base de Graph API
│   ├── accounts.py        # Herramientas de cuentas
│   ├── campaigns.py       # Herramientas de campañas
│   ├── adsets.py          # Herramientas de ad sets
│   ├── ads.py             # Herramientas de anuncios
│   └── insights.py        # Herramientas de insights
├── __init__.py
└── __main__.py            # Punto de entrada
```

## 🛠️ Desarrollo

### Agregar Nueva Herramienta
1. Edita el módulo correspondiente en `meta_ads_mcp/core/`
2. Importa `mcp_server` desde `.server`
3. Aplica decoradores `@mcp_server.tool()` y `@meta_api_tool`
4. Sigue el patrón async con `access_token` opcional
5. Retorna JSON string, no dict

Ejemplo:
```python
@mcp_server.tool()
@meta_api_tool
async def mi_nueva_herramienta(access_token: str = None, param1: str = None) -> str:
    """Descripción de la herramienta"""
    data = await make_api_request("endpoint", access_token, {"param": param1})
    return json.dumps(data, indent=2)
```

### Variables de Entorno Útiles
```bash
# Autenticación
export PIPEBOARD_API_TOKEN=token        # Pipeboard (recomendado)
export META_APP_ID=app_id               # Meta App ID
export META_APP_SECRET=app_secret       # Meta App Secret (opcional)

# Desarrollo
export MCP_LOG_LEVEL=DEBUG              # Logs detallados
export META_GRAPH_API_VERSION=v22.0     # Versión de Graph API
```

## 🔍 Debugging

### Logs Detallados
```bash
# Ver logs detallados
MCP_LOG_LEVEL=DEBUG python -m meta_ads_mcp
```

### Problemas Comunes

#### Error de Autenticación
```bash
# Limpiar tokens cached
rm -rf ~/.config/meta-ads-mcp/  # Linux/Mac
# O eliminar carpeta en Windows: %APPDATA%\meta-ads-mcp\
```

#### Puerto Ocupado
```bash
# Usar puerto diferente
python -m meta_ads_mcp --transport streamable-http --port 8081
```

#### App ID Inválido
```bash
# Verificar App ID
echo $META_APP_ID
# Debe ser un número de ~15 dígitos
```

## 📋 Comandos Útiles

```bash
# Ver versión
python -m meta_ads_mcp --version

# Solo hacer login
python -m meta_ads_mcp --login

# Servidor HTTP con logs
MCP_LOG_LEVEL=DEBUG python -m meta_ads_mcp --transport streamable-http --port 8080

# Prueba completa
python test_meta_ads_auth.py --app-id TU_APP_ID --force-login
```

## 🆘 Soporte

Si tienes problemas:

1. **Verifica las dependencias**: `pip install -e .`
2. **Prueba la autenticación**: `python test_meta_ads_auth.py`
3. **Revisa los logs**: Usa `MCP_LOG_LEVEL=DEBUG`
4. **Consulta la documentación**: [README.md](README.md) y [LOCAL_INSTALLATION.md](LOCAL_INSTALLATION.md)

¡Ya tienes todo listo para desarrollar con Meta Ads MCP! 🎉

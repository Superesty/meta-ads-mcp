# Supabase Video Upload Integration for Meta Ads MCP

Esta documentación describe las nuevas herramientas MCP que permiten subir videos directamente desde el bucket de Supabase de Cogitia hacia la biblioteca de ads de Meta.

## 🎯 Objetivo

Automatizar el proceso de usar el contenido médico/estético almacenado en Cogitia para crear anuncios en Meta Ads, eliminando la necesidad de descargar y subir manualmente los videos.

## 🔧 Nuevas Herramientas MCP

### 1. `list_supabase_videos`

Lista los videos disponibles en el bucket de Supabase de Cogitia.

**Parámetros:**
- `supabase_url` (opcional): URL del proyecto Supabase (default: Cogitia prod)
- `bucket_name` (opcional): Nombre del bucket (default: javier_cano_kno_men_barcelona)
- `category_filter` (opcional): Filtrar por categoría específica

**Ejemplo de uso:**
```python
# Listar todos los videos
result = await list_supabase_videos()

# Listar solo videos de Botox
result = await list_supabase_videos(category_filter="Botox")
```

### 2. `upload_video_from_supabase`

Sube un video desde Supabase hacia la biblioteca de Meta Ads.

**Parámetros:**
- `access_token` (opcional): Token de acceso de Meta API
- `account_id` (requerido): ID de la cuenta de Meta Ads (formato: act_XXXXXXXXX)
- `supabase_video_path` (requerido): Ruta del video en el bucket de Supabase
- `video_title` (opcional): Título del video en Meta Ads
- `supabase_url` (opcional): URL del proyecto Supabase
- `bucket_name` (opcional): Nombre del bucket

**Ejemplo de uso:**
```python
result = await upload_video_from_supabase(
    account_id="act_123456789",
    supabase_video_path="Botox/video/Uso_Botox_Correcto.mp4",
    video_title="Uso Correcto del Botox - Video Educativo"
)
```

### 3. `list_account_videos`

Lista los videos ya subidos en la cuenta de Meta Ads.

**Parámetros:**
- `access_token` (opcional): Token de acceso de Meta API
- `account_id` (requerido): ID de la cuenta de Meta Ads
- `limit` (opcional): Número máximo de videos a retornar (default: 25)
- `fields` (opcional): Campos a retornar para cada video

**Ejemplo de uso:**
```python
result = await list_account_videos(
    account_id="act_123456789",
    limit=10
)
```

## 📁 Estructura del Contenido en Supabase

El bucket de Cogitia contiene las siguientes categorías de videos:

### Categorías Disponibles:
- **Botox** (5 videos) - 49.52 MB
- **Cuidado_de_la_Piel** (11 videos) - 137.98 MB  
- **Acido_Hialuronico** (9 videos) - 102.74 MB
- **Otros_Procedimientos** (10 videos) - 59.33 MB
- **Rejuvenecimiento_Facial** (22 videos) - 200.22 MB

### Ejemplos de Videos:
- `Botox/video/Uso_Botox_Correcto.mp4`
- `Cuidado_de_la_Piel/video/Tratamiento_Piel_Duradero.mp4`
- `Acido_Hialuronico/video/[nombre_del_video].mp4`

## 🚀 Flujo de Trabajo Típico

1. **Explorar contenido disponible:**
   ```python
   videos = await list_supabase_videos(category_filter="Botox")
   ```

2. **Subir video seleccionado:**
   ```python
   upload_result = await upload_video_from_supabase(
       account_id="act_123456789",
       supabase_video_path="Botox/video/Uso_Botox_Correcto.mp4",
       video_title="Botox: Uso Correcto y Seguro"
   )
   ```

3. **Verificar que se subió correctamente:**
   ```python
   account_videos = await list_account_videos(account_id="act_123456789")
   ```

## 🔧 Configuración Técnica

### URLs de Acceso:
- **Supabase URL:** `https://yrbopirjmvukqgsurhxs.supabase.co`
- **Bucket:** `javier_cano_kno_men_barcelona`
- **URL base de videos:** `https://yrbopirjmvukqgsurhxs.supabase.co/storage/v1/object/public/javier_cano_kno_men_barcelona/`

### Endpoint de Meta API:
- **Upload de videos:** `{account_id}/advideos`

## ⚠️ Consideraciones Importantes

1. **Autenticación:** Se requiere un token de acceso válido de Meta API
2. **Formato de Account ID:** Debe incluir el prefijo `act_` (se añade automáticamente si falta)
3. **Tamaño de archivos:** Los videos en Cogitia van desde ~3MB hasta ~19MB
4. **Timeouts:** Se usa un timeout de 60 segundos para la descarga de videos
5. **Logging:** Todas las operaciones se registran para debugging

## 🎯 Beneficios de la Integración

- ✅ **Automatización completa:** No más descarga/subida manual
- ✅ **Calidad preservada:** Los videos mantienen su calidad original
- ✅ **Metadata conservado:** Títulos y descripciones se configuran automáticamente
- ✅ **Workflow eficiente:** Desde contenido médico hasta anuncio en pocos pasos
- ✅ **Trazabilidad:** Logs completos de todas las operaciones

## 📝 Ejemplo Completo de Uso

```python
import asyncio
from meta_ads_mcp.core.ads_library import (
    list_supabase_videos,
    upload_video_from_supabase,
    list_account_videos
)

async def create_botox_campaign_content():
    # 1. Ver qué videos de Botox están disponibles
    available_videos = await list_supabase_videos(category_filter="Botox")
    print("Videos disponibles:", available_videos)
    
    # 2. Subir el video de uso correcto de Botox
    upload_result = await upload_video_from_supabase(
        account_id="act_123456789",
        supabase_video_path="Botox/video/Uso_Botox_Correcto.mp4",
        video_title="Botox: Técnica Correcta y Segura"
    )
    print("Resultado de subida:", upload_result)
    
    # 3. Verificar que el video está en la cuenta
    account_videos = await list_account_videos(account_id="act_123456789")
    print("Videos en la cuenta:", account_videos)

# Ejecutar el ejemplo
asyncio.run(create_botox_campaign_content())
```

## 🔍 Troubleshooting

### Error: "No account ID provided"
- Asegúrate de proporcionar el parámetro `account_id`
- Formato correcto: `act_123456789`

### Error: "Failed to download video from Supabase"
- Verifica que la ruta del video sea correcta
- Comprueba la conectividad a internet
- Usa `list_supabase_videos()` para ver rutas válidas

### Error de autenticación en Meta API
- Verifica que tengas un token de acceso válido
- Asegúrate de que la cuenta de ads tenga permisos para subir videos

## 📊 Estadísticas del Bucket

- **Total de archivos:** 57 videos
- **Tamaño total:** 549.79 MB
- **Formato:** MP4 (compatible con Meta Ads)
- **Contenido:** Videos educativos médicos/estéticos

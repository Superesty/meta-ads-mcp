# Guía de Seguridad - Meta Ads MCP

## ⚠️ Información Sensible

Este proyecto maneja información sensible que **NUNCA** debe estar en el repositorio público:

### 🔒 Datos Confidenciales
- **Access Tokens de Meta**: Tokens de acceso a la API de Meta Ads
- **App ID y App Secret**: Credenciales de aplicación de Meta
- **Tokens de Pipeboard**: Tokens de autenticación de servicios externos
- **Variables de entorno de producción**: Configuraciones con datos reales

### 📁 Archivos Protegidos por .gitignore

```bash
# Archivos de configuración con tokens reales
*.env
.env*
coolify.env
**/secrets.json
**/credentials.json
**/*token*.json
**/*secret*.json
**/*key*.json

# Scripts y configuraciones con datos reales
start_with_token.bat  # (solo la versión con token real)
client-config-production.json  # (solo la versión con token real)
**/production-config.json
```

### ✅ Archivos Seguros (Ejemplos sin datos reales)

Estos archivos están en el repositorio como plantillas:
- `coolify.env.example` - Ejemplo sin tokens reales
- `client-config-production.json` - Con placeholders
- `start_with_token.bat` - Con validación de placeholder

### 🚨 Si Accidentalmente Commites Información Sensible

1. **Revierte inmediatamente**:
   ```bash
   git reset --hard HEAD~1  # Si aún no has hecho push
   ```

2. **Si ya hiciste push**:
   ```bash
   # Crea un commit nuevo removiendo la info sensible
   git add .gitignore archivos_limpios
   git commit -m "SECURITY: Remove sensitive information"
   git push
   ```

3. **Regenera todos los tokens expuestos**:
   - Meta Access Token: Regenera en developers.facebook.com
   - App Secret: Regenera en tu aplicación de Meta
   - Pipeboard Token: Regenera en pipeboard.co

### 📝 Mejores Prácticas

#### Para Desarrollo Local
```bash
# Copia los archivos ejemplo
cp coolify.env.example .env
cp client-config-production.json client-config-local.json

# Edita con tus datos reales (estos archivos están en .gitignore)
# Nunca edites los archivos .example con datos reales
```

#### Para Producción VPS
```bash
# Usa variables de entorno en Coolify
META_ACCESS_TOKEN=tu_token_real_aqui
META_APP_ID=tu_app_id_aqui
META_APP_SECRET=tu_app_secret_aqui
```

#### Para Scripts Locales
```bash
# Crea una copia local del batch script
cp start_with_token.bat start_local.bat
# Edita start_local.bat con tu token real
# start_local.bat está en .gitignore
```

### 🔍 Verificación Antes de Commit

Antes de cada commit, ejecuta:

```bash
# Verifica que no hay tokens reales
grep -r "EAAP" . --exclude-dir=.git
grep -r "107170" . --exclude-dir=.git
grep -r "bcafcd" . --exclude-dir=.git

# Si encuentra resultados, limpia esos archivos antes del commit
```

### 📋 Checklist de Seguridad

Antes de hacer push:

- [ ] ✅ `.env` files están en .gitignore
- [ ] ✅ No hay tokens reales en archivos commiteados
- [ ] ✅ Solo archivos `.example` tienen placeholders
- [ ] ✅ Scripts batch locales están en .gitignore
- [ ] ✅ Configuraciones de producción están excluidas
- [ ] ✅ Ejecuté `grep` para verificar no hay tokens

### 🆘 Contacto de Emergencia

Si detectas una exposición de seguridad:
1. Reporta inmediatamente al administrador del repositorio
2. Documenta qué información fue expuesta
3. Lista qué tokens necesitan regeneración
4. Confirma que los datos han sido removidos del historial

---

**Recuerda**: Es mejor ser excesivamente cauteloso con la seguridad que lamentar una exposición de datos.

# Guía de Configuración - InfoMilo

Esta guía te ayudará a configurar el proyecto InfoMilo para trabajo remoto, adaptándose tanto al trabajo desde casa como desde la oficina.

## 📋 Requisitos Previos

### Software Necesario
- **Node.js** (v16 o superior) - [Descargar](https://nodejs.org/)
- **Git** - [Descargar](https://git-scm.com/)
- **PowerShell** (Windows) o **Bash** (Linux/Mac)
- **Visual Studio Code** - [Descargar](https://code.visualstudio.com/)

### Extensiones de VS Code Recomendadas
El proyecto incluye una lista de extensiones recomendadas que se instalarán automáticamente:
- GitHub Copilot
- Prettier
- PowerShell
- Remote SSH
- Live Server
- Material Icon Theme

## 🚀 Configuración Inicial

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd InfoMilo
```

### 2. Ejecutar Setup Automático
```powershell
# Configuración por defecto
.\scripts\setup.ps1

# O específica para casa/oficina
.\scripts\setup.ps1 -Environment home
.\scripts\setup.ps1 -Environment office
```

### 3. Configurar Variables de Entorno
1. Copia `.env.example` a `.env`
2. Edita `.env` with tus configuraciones específicas

## 🏠 Configuración para Casa

### Características de la Configuración de Casa
- **Puerto**: 3000 (puerto estándar para desarrollo)
- **Proxy**: Deshabilitado
- **Debug**: Habilitado para desarrollo activo
- **Backup**: Sincronización en la nube habilitada
- **Tema**: Oscuro (mejor para trabajar en casa)

### Activar Configuración de Casa
```powershell
.\scripts\switch-env.ps1 home
```

O usar la tarea de VS Code: `Ctrl+Shift+P` > `Tasks: Run Task` > `Switch to Home Config`

## 🏢 Configuración para Oficina

### Características de la Configuración de Oficina
- **Puerto**: 8080 (evita conflictos con proxy corporativo)
- **Proxy**: Configurado para red corporativa
- **VPN**: Requerida para recursos internos
- **Debug**: Limitado por políticas de seguridad
- **Backup**: Solo local y unidad de red corporativa
- **Tema**: Claro (mejor para oficina bien iluminada)

### Activar Configuración de Oficina
```powershell
.\scripts\switch-env.ps1 office
```

O usar la tarea de VS Code: `Ctrl+Shift+P` > `Tasks: Run Task` > `Switch to Office Config`

## ⚙️ Configuraciones Personalizadas

### Modificar Configuraciones
Las configuraciones están en archivos JSON en la carpeta `config/`:
- `home.json` - Configuración para casa
- `office.json` - Configuración para oficina
- `default.json` - Configuración por defecto

### Estructura de Configuración
```json
{
    "environment": "nombre",
    "network": {
        "proxy": true/false,
        "proxy_url": "url del proxy",
        "vpn": true/false
    },
    "development": {
        "port": 3000,
        "host": "localhost",
        "debug_mode": true
    },
    "paths": {
        "workspace": "ruta del workspace",
        "temp": "ruta temporal",
        "logs": "ruta de logs"
    }
}
```

## 🔧 Troubleshooting

### Problemas Comunes

#### Error de Puerto Ocupado
```powershell
# Cambiar puerto en la configuración activa
# Editar config/active.json y cambiar "port": 3001
```

#### Problemas de Proxy
```powershell
# Verificar configuración de proxy
npm config list
# Configurar proxy si es necesario
npm config set proxy http://proxy.empresa.com:8080
```

#### Permisos de PowerShell
```powershell
# Si hay errores de ejecución de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Logs y Debug
Los logs se guardan en la carpeta `logs/` según la configuración activa.

```powershell
# Ver logs recientes
Get-Content logs/error.log -Tail 10
```

## 📱 Sincronización Entre Entornos

### Archivos que se Sincronizan
- Código fuente (`src/`)
- Configuraciones de proyecto (`.vscode/`, `.github/`)
- Documentación (`docs/`)

### Archivos que NO se Sincronizan
- Variables de entorno (`.env`)
- Configuración activa (`config/active.json`)
- Dependencias (`node_modules/`)
- Archivos temporales (`temp/`, `logs/`)

### Mejores Prácticas
1. **Commit frecuente** - Mantén el código sincronizado
2. **Branch por ubicación** - Opcional: usa branches para trabajo específico
3. **Stash antes de cambiar** - Guarda cambios locales antes de pull
4. **Test en ambos entornos** - Verifica que funcione en casa y oficina

## 🔐 Seguridad

### Configuración de Casa
- Variables sensibles en `.env` (nunca en Git)
- VPN personal si es necesario
- Backup cifrado en la nube

### Configuración de Oficina
- Cumplimiento de políticas corporativas
- Certificados de empresa configurados
- Solo backup en unidades autorizadas

## 📞 Soporte

Si tienes problemas:
1. Consulta esta guía
2. Revisa los logs en `logs/`
3. Busca en los issues del repositorio
4. Contacta al equipo de desarrollo

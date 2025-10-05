# 🔐 InfoMilo - Sistema de Autenticación Completo

## 📋 Características Implementadas

### ✅ Sistema de Autenticación Avanzado
- **Login seguro** con email/usuario y contraseña
- **Registro de usuarios** con validación de email
- **Recuperación de contraseña** vía email (Gmail SMTP)
- **Cambio de contraseña** con validación de fortaleza
- **Autenticación en dos pasos (2FA)** opcional por usuario
- **Control de intentos fallidos** (máximo 3 intentos)
- **Sesiones con expiración** automática
- **Contraseñas con hash bcrypt** para máxima seguridad

### 👥 Gestión de Usuarios y Roles
- **Roles específicos**: admin y user con permisos diferenciados
- **Un usuario = un rol** (no roles múltiples)
- **Panel de administración** para gestión de usuarios
- **Perfil de usuario** editable con información adicional
- **Activación/desactivación** de cuentas

### 📧 Sistema de Notificaciones Email
- **Gmail SMTP** configurado y listo para usar
- **Email de bienvenida** al registrarse
- **Email de recuperación** de contraseña
- **Alertas de seguridad** por login sospechoso
- **Notificaciones** de cambios importantes

### 📊 Auditoría Completa
- **Registro de eventos** de autenticación
- **Información detallada**: IP, navegador, ubicación
- **Logs automáticos** de login, logout, cambios
- **Conservación de 6 meses** con limpieza automática
- **Dashboard de actividad** para usuarios y administradores

### 🎨 Interfaz Moderna e Institucional
- **Páginas separadas** para cada función
- **Diseño responsive** con Bootstrap 5
- **Estilo moderno** y profesional
- **Componentes institucionales** con colores corporativos
- **Experiencia de usuario** optimizada

### 🏠 Trabajo Flexible Casa/Oficina
- **Base de datos compartida** entre entornos
- **Configuración automática** por ubicación
- **Sincronización** de configuraciones
- **Scripts automáticos** para cambio de entorno

## ✅ Estado Actual (Octubre 2025)

### 🎯 Completamente Funcional
- ✅ **Aplicación Flask ejecutándose** en http://localhost:3000
- ✅ **Todas las plantillas HTML** creadas y funcionando
- ✅ **Sistema de autenticación** completamente implementado
- ✅ **Base de datos SQLite** inicializada y configurada
- ✅ **Rutas de autenticación** corregidas y funcionando
- ✅ **Filtros de fecha** personalizados implementados
- ✅ **Panel de administración** de usuarios funcional
- ✅ **Documentación técnica** actualizada

### 🔧 Pendientes Menores
- ⚠️ **Variables de entorno Gmail** por configurar (opcional para testing)
- 📧 **Pruebas de envío de email** real con credenciales Gmail
- 🧪 **Testing completo de flujos** de registro y recuperación
- 🔄 **Sincronización de entornos** casa/oficina

### 📊 Endpoints Disponibles
- 🏠 **Home**: http://localhost:3000/
- 🔐 **Login**: http://localhost:3000/auth/login
- 📝 **Registro**: http://localhost:3000/auth/register
- 👤 **Perfil**: http://localhost:3000/auth/profile
- ⚙️ **Admin**: http://localhost:3000/auth/admin/users
- 📖 **Docs**: http://localhost:3000/docs
- 📊 **API Status**: http://localhost:3000/api/status

## 🚀 Inicio Rápido

### 1. Configuración Inicial
```powershell
# Clonar el proyecto (si viene de Git)
git clone https://github.com/tu-usuario/InfoMilo.git
cd InfoMilo

# O ejecutar setup automático desde oficina
.\scripts\setup-office.ps1
```

### 2. Configurar Variables de Entorno
```powershell
# Copiar ejemplo de configuración
copy .env.example .env

# Editar .env con tus datos:
# - SECRET_KEY: clave secreta para Flask
# - MAIL_USERNAME: tu email de Gmail
# - MAIL_PASSWORD: App Password de Gmail
# - APP_URL: URL base de tu aplicación
```

### 3. Iniciar Aplicación
```powershell
# Método 1: Script automático
.\scripts\work-manager.ps1
# Seleccionar opción 3: "Iniciar trabajo en oficina"

# Método 2: Manual
.venv\Scripts\activate
python src\app.py
```

### 4. Acceder al Sistema
- **URL**: http://localhost:3000
- **Admin**: admin@infomilo.com / admin123
- **Registrar nuevos usuarios** desde la página principal

## 📚 Documentación de Usuario

### 🔑 Credenciales por Defecto
Al iniciar por primera vez, se crea automáticamente:
- **Usuario**: admin@infomilo.com
- **Contraseña**: admin123
- **Rol**: Administrador

> ⚠️ **IMPORTANTE**: Cambiar la contraseña del administrador inmediatamente después del primer login.

### 👤 Flujo de Usuario Regular

1. **Registro**:
   - Ir a http://localhost:3000
   - Clic en "Registrarse"
   - Completar formulario (usuario, email, contraseña)
   - Confirmar email si está configurado

2. **Login**:
   - Email/usuario + contraseña
   - Código 2FA si está activado
   - Recordar sesión (opcional)

3. **Dashboard**:
   - Resumen de cuenta y actividad
   - Acceso a configuración personal
   - Gestión de seguridad

4. **Perfil**:
   - Editar información personal
   - Cambiar contraseña
   - Configurar 2FA

### 👨‍💼 Funciones de Administrador

1. **Gestión de Usuarios**:
   - Ver todos los usuarios registrados
   - Activar/desactivar cuentas
   - Cambiar roles
   - Resetear contraseñas

2. **Monitoreo**:
   - Ver logs de auditoría
   - Actividad de usuarios
   - Estadísticas del sistema

3. **Configuración**:
   - Cambiar configuración de entorno
   - Gestionar configuraciones del sistema

## ⚙️ Configuración Técnica

### 🗄️ Base de Datos
- **SQLite** para desarrollo (archivo: `data/infomilo.db`)
- **Tablas principales**:
  - `users`: Información de usuarios
  - `roles`: Roles del sistema (admin, user)
  - `audit_logs`: Registro de eventos
  - `password_resets`: Tokens de recuperación

### 📧 Configuración Email (Gmail)
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
```

> 📋 **Nota**: Necesitas generar un "App Password" en tu cuenta de Gmail, no uses tu contraseña normal.

### 🔒 Configuración de Seguridad
```env
SECRET_KEY=clave_super_secreta_aqui
PASSWORD_MIN_LENGTH=8
MAX_LOGIN_ATTEMPTS=3
SESSION_TIMEOUT=3600
```

### 🌍 Configuración de Entorno
Archivos en `config/`:
- `home.json`: Configuración para casa
- `office.json`: Configuración para oficina
- `active.json`: Configuración actualmente activa

## 🛠️ Scripts Automáticos

### Para Oficina:
```powershell
# Iniciar trabajo en oficina
.\scripts\work-manager.ps1  # Opción 3

# Cambiar a configuración oficina
.\scripts\switch-to-office.ps1

# Terminar trabajo en oficina
.\scripts\end-work-office.ps1
```

### Para Casa:
```powershell
# Iniciar trabajo en casa
.\scripts\work-manager.ps1  # Opción 1

# Cambiar a configuración casa
.\scripts\switch-to-home.ps1

# Terminar trabajo en casa
.\scripts\end-work-home.ps1
```

## 🔐 Características de Seguridad

### Autenticación
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Control de intentos fallidos (3 máximo)
- ✅ Bloqueo temporal de cuentas
- ✅ Sesiones con expiración (1 hora por defecto)
- ✅ 2FA opcional con código TOTP

### Auditoría
- ✅ Registro de todos los eventos de login/logout
- ✅ Captura de IP, navegador, OS
- ✅ Detección de logins sospechosos
- ✅ Logs con retención de 6 meses
- ✅ Limpieza automática de logs antiguos

### Comunicaciones
- ✅ Emails seguros via Gmail SMTP
- ✅ Tokens de recuperación con expiración
- ✅ Notificaciones de cambios de seguridad
- ✅ Alertas de actividad sospechosa

## 📱 Endpoints Disponibles

### Públicos:
- `GET /` - Página principal
- `GET /auth/login` - Página de login
- `GET /auth/register` - Página de registro
- `GET /auth/forgot-password` - Recuperación de contraseña
- `GET /api/status` - Estado del sistema

### Autenticados:
- `GET /dashboard` - Dashboard principal
- `GET /auth/profile` - Perfil de usuario
- `GET /auth/change-password` - Cambiar contraseña
- `GET /auth/setup-2fa` - Configurar 2FA
- `POST /auth/logout` - Cerrar sesión

### Administrador:
- `GET /auth/admin/users` - Gestión de usuarios
- `POST /api/switch-env` - Cambiar configuración

## 🐛 Troubleshooting

### Error: "No se puede conectar"
```powershell
# Verificar que el servidor esté corriendo
netstat -ano | findstr :3000

# Reiniciar aplicación
python src\app.py
```

### Error: "Email no se envía"
1. Verificar configuración en `.env`
2. Generar App Password en Gmail
3. Verificar que SMTP esté habilitado

### Error: "Base de datos bloqueada"
```powershell
# Detener todos los procesos Python
taskkill /f /im python.exe

# Reiniciar aplicación
python src\app.py
```

### Error: "2FA no funciona"
1. Verificar que el tiempo del sistema sea correcto
2. Regenerar código QR en configuración
3. Usar aplicación compatible (Google Authenticator, Authy)

## 📈 Próximas Mejoras

- [ ] Dashboard de analytics avanzado
- [ ] Integración con Active Directory
- [ ] API REST completa
- [ ] App móvil
- [ ] Notificaciones push
- [ ] Backup automático de BD
- [ ] Logs centralizados
- [ ] Métricas de performance

## 🤝 Soporte

Para soporte técnico:
1. Revisa esta documentación
2. Consulta los logs en `logs/`
3. Verifica la configuración en `config/`
4. Ejecuta `python test_imports.py` para diagnóstico

---

## 📜 Licencia

Este proyecto es de uso interno para InfoMilo.

**© 2024 InfoMilo - Sistema de Trabajo Remoto Flexible**

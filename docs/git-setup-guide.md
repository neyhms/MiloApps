# 🔗 Configurar Repositorio Git para InfoMilo

## 🎯 Objetivo
Configurar un repositorio Git para sincronizar InfoMilo entre casa y oficina.

---

## 🚀 OPCIÓN 1: GitHub (Recomendado)

### Paso 1: Crear repositorio en GitHub
1. Ir a [github.com](https://github.com)
2. Click en "New repository"
3. Nombre: `InfoMilo`
4. Descripción: `Proyecto flexible para trabajo remoto casa/oficina`
5. ✅ Marcar "Private" (si quieres que sea privado)
6. ❌ NO marcar "Add README" (ya tienes uno)
7. Click "Create repository"

### Paso 2: Conectar tu proyecto local
```powershell
# En tu ordenador de casa (carpeta InfoMilo):
git remote add origin https://github.com/neyhms/InfoMilo.git
git branch -M main
git push -u origin main
```

### Paso 3: Clonar en oficina
```powershell
# En oficina:
git clone https://github.com/neyhms/InfoMilo.git
cd InfoMilo
# Continuar con setup de oficina...
```

---

## 🔧 OPCIÓN 2: GitLab

### Paso 1: Crear proyecto en GitLab
1. Ir a [gitlab.com](https://gitlab.com)
2. Click "New project" → "Create blank project"
3. Project name: `InfoMilo`
4. Visibility: Private
5. ❌ NO marcar "Initialize repository with a README"
6. Create project

### Paso 2: Conectar proyecto local
```powershell
git remote add origin https://gitlab.com/neyhms/InfoMilo.git
git branch -M main
git push -u origin main
```

---

## 🏢 OPCIÓN 3: Servidor Corporativo

Si tu empresa tiene GitLab/Azure DevOps/Bitbucket:

```powershell
# Ejemplo Azure DevOps:
git remote add origin https://dev.azure.com/tu-empresa/InfoMilo/_git/InfoMilo

# Ejemplo GitLab corporativo:
git remote add origin https://gitlab.empresa.com/tu-usuario/InfoMilo.git

# Ejemplo Bitbucket:
git remote add origin https://bitbucket.org/tu-usuario/infomilo.git
```

---

## ✅ Verificar configuración

```powershell
# Ver remote configurado
git remote -v

# Debería mostrar algo como:
# origin  https://github.com/neyhms/InfoMilo.git (fetch)
# origin  https://github.com/neyhms/InfoMilo.git (push)
```

---

## 🔄 Flujo de trabajo diario

### Desde casa:
```powershell
# Al empezar el día
git pull origin main

# Al terminar el día
git add .
git commit -m "feat: trabajo desde casa - [descripción]"
git push origin main
```

### Desde oficina:
```powershell
# Al empezar el día
git pull origin main

# Al terminar el día
git add .
git commit -m "feat: trabajo desde oficina - [descripción]"
git push origin main
```

---

## 🚨 Comandos importantes

### Resolver conflictos:
```powershell
# Si hay conflictos al hacer pull
git pull origin main
# Resolver conflictos manualmente en VS Code
git add .
git commit -m "resolve: merge conflicts"
git push origin main
```

### Backup de seguridad:
```powershell
# Crear branch de backup antes de cambios importantes
git checkout -b backup-$(Get-Date -Format "yyyy-MM-dd")
git push origin backup-$(Get-Date -Format "yyyy-MM-dd")
git checkout main
```

### Ver historial:
```powershell
# Ver commits recientes
git log --oneline -10

# Ver cambios en archivos
git status
git diff
```

---

## 📋 Estados después de configurar Git

### ✅ El proyecto tendrá:
- Repositorio Git inicializado ✅
- Remote origin configurado ✅
- Sincronización entre casa/oficina ✅
- Historial de cambios ✅
- Backup automático en la nube ✅

### 🔄 Scripts automáticos funcionarán:
- Los scripts `start-work-*` y `end-work-*` incluyen `git pull` y `git push`
- Sincronización automática al empezar/terminar trabajo
- Detección de cambios pendientes

---

## 🎯 Recomendación

**Para empezar rápido:** Usa GitHub (gratuito, fácil, confiable)

1. Crear repositorio: 2 minutos
2. Configurar remote: 1 comando
3. Push inicial: 1 comando
4. ¡Listo para sincronizar entre casa y oficina!

**URL final sería:** `https://github.com/neyhms/InfoMilo.git`

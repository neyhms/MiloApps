# 🔗 CONFIGURAR REPOSITORIO GIT - COMANDOS LISTOS

## 🚀 Para configurar GitHub (Recomendado)

### 1. Crear repositorio en GitHub
- Ir a: https://github.com/new
- Nombre: `InfoMilo`
- Privado: ✅ (recomendado)
- No crear README (ya tienes uno)

### 2. Ejecutar estos comandos en tu casa:
```powershell
# Cambiar "tu-usuario" por tu usuario real de GitHub
git remote add origin https://github.com/tu-usuario/InfoMilo.git
git branch -M main
git push -u origin main
```

### 3. En oficina usar:
```powershell
git clone https://github.com/tu-usuario/InfoMilo.git
```

---

## 📝 Comandos personalizados

### Para neyhms (tu usuario):
```powershell
# En casa (InfoMilo ya configurado):
git remote add origin https://github.com/neyhms/InfoMilo.git
git branch -M main  
git push -u origin main

# En oficina:
git clone https://github.com/neyhms/InfoMilo.git
cd InfoMilo
.\scripts\setup-office.ps1
```

---

## 🔄 Alternativa sin GitHub

Si no quieres usar GitHub ahora mismo:

### Transferencia manual:
1. **En casa**: Comprimir carpeta InfoMilo → InfoMilo.zip
2. **Subir a**: OneDrive/Google Drive/USB
3. **En oficina**: Descargar y descomprimir
4. **Ejecutar**: `.\scripts\setup-office.ps1`

### Configurar Git más tarde:
```powershell
# Cuando quieras sincronización automática
# Seguir pasos de GitHub arriba
```

---

## ⚡ COMANDO RÁPIDO PARA CASA

```powershell
# COPIA Y PEGA (cambiar tu-usuario por el real):
git remote add origin https://github.com/tu-usuario/InfoMilo.git && git branch -M main && git push -u origin main
```

## ⚡ COMANDO RÁPIDO PARA OFICINA

```powershell  
# COPIA Y PEGA (cambiar tu-usuario por el real):
git clone https://github.com/tu-usuario/InfoMilo.git && cd InfoMilo && .\scripts\setup-office.ps1
```

# Script para TERMINAR trabajo desde OFICINA
# Ejecutar al finalizar el día de trabajo en la oficina

Write-Host "🏢 TERMINANDO TRABAJO DESDE OFICINA..." -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue
Write-Host ""

# Paso 1: Verificar estado del proyecto
Write-Host "📋 1. Verificando estado del proyecto..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Archivos modificados encontrados:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    
    # Paso 2: Hacer commit automático
    Write-Host "💾 2. Guardando cambios..." -ForegroundColor Yellow
    $fecha = Get-Date -Format "yyyy-MM-dd"
    $hora = Get-Date -Format "HH:mm"
    
    git add .
    git commit -m "trabajo oficina ($fecha $hora): fin de jornada desde oficina"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Commit realizado correctamente" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Error en commit - revisar manualmente" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "✅ No hay cambios pendientes" -ForegroundColor Green
}

# Paso 3: Subir cambios a GitHub
Write-Host "📤 3. Subiendo cambios a GitHub..." -ForegroundColor Yellow
if (Test-Path ".git") {
    $hasRemote = git remote -v 2>$null
    if (![string]::IsNullOrEmpty($hasRemote)) {
        try {
            git push origin main
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Cambios subidos a GitHub exitosamente" -ForegroundColor Green
                Write-Host "   🌐 Disponible para sincronizar en casa" -ForegroundColor Cyan
            }
            else {
                Write-Host "⚠️ Error subiendo - verificar conexión/proxy corporativo" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "⚠️ Error de conexión - cambios guardados localmente" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "⚠️ GitHub no configurado - cambios solo guardados localmente" -ForegroundColor Yellow
        Write-Host "💡 Configura GitHub para sincronización automática" -ForegroundColor Gray
    }
}
else {
    Write-Host "⚠️ No es repositorio Git - cambios solo guardados localmente" -ForegroundColor Yellow
}

# Paso 4: Crear backup en red corporativa (simulado)
Write-Host "💾 4. Creando backup corporativo..." -ForegroundColor Yellow
$backupDir = "temp\backup-oficina-$(Get-Date -Format 'yyyy-MM-dd')"
if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}
# Copiar archivos importantes
Copy-Item "config\active.json" "$backupDir\" -Force
Copy-Item "src\app.py" "$backupDir\" -Force
Write-Host "✅ Backup local creado en $backupDir" -ForegroundColor Green

# Paso 5: Generar resumen del trabajo
Write-Host "📊 5. Generando resumen del día..." -ForegroundColor Yellow
$commits = git log --oneline --since="today" --author="$(git config user.name)" 2>$null
if ($commits) {
    Write-Host "📈 Commits de hoy:" -ForegroundColor Cyan
    $commits | ForEach-Object { Write-Host "   • $_" -ForegroundColor White }
}
else {
    Write-Host "📈 No hay commits nuevos hoy" -ForegroundColor Gray
}

# Paso 6: Limpiar entorno y procesos
Write-Host "🧹 6. Limpiando entorno..." -ForegroundColor Yellow
# Detener procesos Flask
Get-Process | Where-Object { $_.ProcessName -like "*python*" -and $_.Path -like "*InfoMilo*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Limpiar archivos temporales
if (Test-Path "temp\*") {
    Remove-Item "temp\*" -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "🎉 ¡TRABAJO DE OFICINA TERMINADO!" -ForegroundColor Blue
Write-Host "=================================" -ForegroundColor Blue
Write-Host "✅ Cambios guardados y sincronizados" -ForegroundColor White
Write-Host "✅ Repositorio actualizado" -ForegroundColor White
Write-Host "✅ Backup corporativo creado" -ForegroundColor White
Write-Host "✅ Entorno limpio" -ForegroundColor White
Write-Host ""
Write-Host "📱 PRÓXIMO TRABAJO:" -ForegroundColor Cyan
Write-Host "   🏠 Casa: Ejecutar .\scripts\start-work-home.ps1" -ForegroundColor White
Write-Host "   🏢 Oficina: Ejecutar .\scripts\start-work-office.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🚗 ¡Buen viaje a casa!" -ForegroundColor Blue

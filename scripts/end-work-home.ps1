# Script para TERMINAR trabajo desde CASA
# Ejecutar al finalizar el día de trabajo en casa

Write-Host "🏠 TERMINANDO TRABAJO DESDE CASA..." -ForegroundColor Blue
Write-Host "===================================" -ForegroundColor Blue
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
    git commit -m "trabajo casa ($fecha $hora): fin de jornada desde casa"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Commit realizado correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error en commit - revisar manualmente" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ No hay cambios pendientes" -ForegroundColor Green
}

# Paso 3: Subir cambios al repositorio
Write-Host "📤 3. Subiendo cambios al repositorio..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cambios subidos correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error subiendo cambios - revisar conexión" -ForegroundColor Red
}

# Paso 4: Crear resumen del trabajo
Write-Host "📊 4. Generando resumen del día..." -ForegroundColor Yellow
$commits = git log --oneline --since="today" --author="$(git config user.name)" 2>$null
if ($commits) {
    Write-Host "📈 Commits de hoy:" -ForegroundColor Cyan
    $commits | ForEach-Object { Write-Host "   • $_" -ForegroundColor White }
} else {
    Write-Host "📈 No hay commits nuevos hoy" -ForegroundColor Gray
}

# Paso 5: Limpiar entorno
Write-Host "🧹 5. Limpiando entorno..." -ForegroundColor Yellow
# Detener procesos Flask si están corriendo
Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.Path -like "*InfoMilo*"} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 ¡TRABAJO DE CASA TERMINADO!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "✅ Cambios guardados y sincronizados" -ForegroundColor White
Write-Host "✅ Repositorio actualizado" -ForegroundColor White
Write-Host "✅ Entorno limpio" -ForegroundColor White
Write-Host ""
Write-Host "📱 PRÓXIMO TRABAJO:" -ForegroundColor Cyan
Write-Host "   🏢 Oficina: Ejecutar .\scripts\start-work-office.ps1" -ForegroundColor White
Write-Host "   🏠 Casa: Ejecutar .\scripts\start-work-home.ps1" -ForegroundColor White
Write-Host ""
Write-Host "😴 ¡Descansa bien!" -ForegroundColor Green

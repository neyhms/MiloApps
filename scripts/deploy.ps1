# InfoMilo Deploy Script
# Script para desplegar el proyecto

param(
    [string]$Target = "staging",
    [switch]$Production
)

Write-Host "🚀 Iniciando despliegue de InfoMilo..." -ForegroundColor Green
Write-Host ""

if ($Production) {
    $Target = "production"
    Write-Host "⚠️  MODO PRODUCCIÓN ACTIVADO" -ForegroundColor Red
    $confirmation = Read-Host "¿Estás seguro de que quieres desplegar a producción? (s/N)"
    if ($confirmation -ne "s" -and $confirmation -ne "S") {
        Write-Host "❌ Despliegue cancelado" -ForegroundColor Yellow
        exit 0
    }
}

# Ejecutar tests antes del despliegue
Write-Host "🧪 Ejecutando tests..." -ForegroundColor Cyan
npm test
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Los tests fallaron. Despliegue cancelado." -ForegroundColor Red
    exit 1
}

# Construir el proyecto
Write-Host "🔨 Construyendo el proyecto..." -ForegroundColor Cyan
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error en la construcción. Despliegue cancelado." -ForegroundColor Red
    exit 1
}

# Simular despliegue (aquí irían los comandos reales de despliegue)
Write-Host "📦 Desplegando a $Target..." -ForegroundColor Cyan
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ ¡Despliegue completado exitosamente!" -ForegroundColor Green
Write-Host "   Target: $Target" -ForegroundColor Gray
Write-Host "   Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

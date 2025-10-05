# Script automático para crear repositorio MiloApps
Write-Host "🚀 CREANDO REPOSITORIO MILOAPPS..." -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Abrir GitHub en la página de crear repositorio con parámetros
$repoUrl = "https://github.com/new?name=MiloApps&description=%F0%9F%90%B1%20MiloApps%20-%20Sistema%20de%20autenticaci%C3%B3n%20avanzado%20con%20Flask&visibility=private"

Write-Host "🌐 Abriendo GitHub para crear repositorio..." -ForegroundColor Yellow
Start-Process $repoUrl

Write-Host ""
Write-Host "📋 DATOS PRE-LLENADOS:" -ForegroundColor Cyan
Write-Host "   📁 Nombre: MiloApps" -ForegroundColor White
Write-Host "   📝 Descripción: 🐱 MiloApps - Sistema de autenticación avanzado con Flask" -ForegroundColor White
Write-Host "   🔒 Privado: Sí" -ForegroundColor White
Write-Host ""
Write-Host "⚡ SOLO TIENES QUE:" -ForegroundColor Yellow
Write-Host "   1. Click en 'Create repository' (verde)" -ForegroundColor White
Write-Host "   2. Esperar 5 segundos" -ForegroundColor White
Write-Host ""

# Esperar a que el usuario cree el repositorio
Write-Host "⏳ Esperando 15 segundos para que crees el repositorio..." -ForegroundColor Yellow
for ($i = 15; $i -gt 0; $i--) {
    Write-Host "   $i segundos restantes..." -ForegroundColor Gray
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "📤 Subiendo código a GitHub..." -ForegroundColor Green

# Intentar hacer push varias veces
$maxRetries = 3
$retry = 0
$success = $false

while ($retry -lt $maxRetries -and !$success) {
    try {
        $retry++
        Write-Host "   Intento $retry de $maxRetries..." -ForegroundColor Yellow
        
        $result = git push -u origin main 2>&1
        if ($LASTEXITCODE -eq 0) {
            $success = $true
            Write-Host "🎉 ¡CÓDIGO SUBIDO EXITOSAMENTE!" -ForegroundColor Green
        }
        else {
            Write-Host "   ⚠️ Error en intento $retry" -ForegroundColor Yellow
            if ($retry -lt $maxRetries) {
                Write-Host "   ⏳ Esperando 5 segundos..." -ForegroundColor Gray
                Start-Sleep -Seconds 5
            }
        }
    }
    catch {
        Write-Host "   ❌ Error en intento $retry" -ForegroundColor Red
        if ($retry -lt $maxRetries) {
            Start-Sleep -Seconds 5
        }
    }
}

if ($success) {
    Write-Host ""
    Write-Host "✅ ¡GITHUB CONFIGURADO COMPLETAMENTE!" -ForegroundColor Green
    Write-Host "🔗 Tu repositorio: https://github.com/neyhms/MiloApps" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🏠 TRABAJO DESDE CASA LISTO:" -ForegroundColor Cyan
    Write-Host "   • Sincronización automática configurada" -ForegroundColor White
    Write-Host "   • Scripts de inicio/cierre funcionando" -ForegroundColor White
    Write-Host "   • MiloApps ejecutándose en localhost:3000" -ForegroundColor White
}
else {
    Write-Host ""
    Write-Host "❌ No se pudo subir automáticamente" -ForegroundColor Red
    Write-Host "🔧 Ejecuta manualmente: git push -u origin main" -ForegroundColor Yellow
    Write-Host "🔗 Repositorio: https://github.com/neyhms/MiloApps" -ForegroundColor Cyan
}

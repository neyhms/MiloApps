# Script MAESTRO para MiloApps
# Menu principal para gestionar trabajo desde casa y oficina

Write-Host ""
Write-Host "🐱 MILOAPPS - GESTOR DE TRABAJO REMOTO" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Detectar configuracion actual
$currentConfig = "desconocida"
if (Test-Path "config\active.json") {
    $config = Get-Content "config\active.json" | ConvertFrom-Json
    $currentConfig = $config.environment
}

Write-Host "📍 Configuracion actual: " -NoNewline -ForegroundColor Yellow
if ($currentConfig -eq "home") {
    Write-Host "🏠 CASA" -ForegroundColor Green
}
elseif ($currentConfig -eq "office") {
    Write-Host "🏢 OFICINA" -ForegroundColor Blue
}
else {
    Write-Host "❓ $currentConfig" -ForegroundColor Gray
}

Write-Host ""
Write-Host "¿Que quieres hacer?" -ForegroundColor Cyan
Write-Host ""
Write-Host "🏠 TRABAJO DESDE CASA:" -ForegroundColor Green
Write-Host "  1. Iniciar trabajo en casa" -ForegroundColor White
Write-Host "  2. Terminar trabajo en casa" -ForegroundColor White
Write-Host ""
Write-Host "🏢 TRABAJO DESDE OFICINA:" -ForegroundColor Blue
Write-Host "  3. Iniciar trabajo en oficina" -ForegroundColor White
Write-Host "  4. Terminar trabajo en oficina" -ForegroundColor White
Write-Host ""
Write-Host "⚙️ CONFIGURACION:" -ForegroundColor Yellow
Write-Host "  5. Cambiar a configuracion casa" -ForegroundColor White
Write-Host "  6. Cambiar a configuracion oficina" -ForegroundColor White
Write-Host "  7. Ver estado del proyecto" -ForegroundColor White
Write-Host ""
Write-Host "🔗 GIT Y GITHUB:" -ForegroundColor Magenta
Write-Host "  8. Sincronizar con GitHub" -ForegroundColor White
Write-Host "  9. Solo descargar cambios" -ForegroundColor White
Write-Host "  10. Solo subir cambios" -ForegroundColor White
Write-Host ""
Write-Host "🚀 MILOAPPS:" -ForegroundColor Cyan
Write-Host "  11. Iniciar servidor MiloApps" -ForegroundColor White
Write-Host "  12. Abrir MiloApps en navegador" -ForegroundColor White
Write-Host ""
Write-Host "  0. Salir" -ForegroundColor White
Write-Host ""

$opcion = Read-Host "Selecciona una opcion (0-12)"

switch ($opcion) {
    "1" {
        Write-Host "🏠 Iniciando trabajo desde CASA..." -ForegroundColor Green
        powershell -ExecutionPolicy Bypass -File "scripts\start-home-simple.ps1"
    }
    "2" {
        Write-Host "🏠 Terminando trabajo desde CASA..." -ForegroundColor Green
        powershell -ExecutionPolicy Bypass -File "scripts\end-work-home.ps1"
    }
    "3" {
        Write-Host "🏢 Iniciando trabajo desde OFICINA..." -ForegroundColor Blue
        powershell -ExecutionPolicy Bypass -File "scripts\start-work-office.ps1"
    }
    "4" {
        Write-Host "🏢 Terminando trabajo desde OFICINA..." -ForegroundColor Blue
        powershell -ExecutionPolicy Bypass -File "scripts\end-work-office.ps1"
    }
    "5" {
        Write-Host "🏠 Cambiando a configuracion de CASA..." -ForegroundColor Yellow
        Copy-Item -Path "config\home.json" -Destination "config\active.json" -Force
        Write-Host "✅ Configuracion de CASA activada" -ForegroundColor Green
    }
    "6" {
        Write-Host "🏢 Cambiando a configuracion de OFICINA..." -ForegroundColor Yellow
        Copy-Item -Path "config\office.json" -Destination "config\active.json" -Force
        Write-Host "✅ Configuracion de OFICINA activada" -ForegroundColor Green
    }
    "7" {
        Write-Host "📊 ESTADO DEL PROYECTO:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📁 Configuracion actual:" -ForegroundColor Yellow
        if (Test-Path "config\active.json") {
            $config = Get-Content "config\active.json" | ConvertFrom-Json
            Write-Host "   Entorno: $($config.environment)" -ForegroundColor White
            Write-Host "   Puerto: $($config.development.port)" -ForegroundColor White
            Write-Host "   Debug: $($config.development.debug_mode)" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "📈 Estado de Git:" -ForegroundColor Yellow
        git status --porcelain
        Write-Host ""
        Write-Host "🐍 Entorno Python:" -ForegroundColor Yellow
        if (Test-Path ".venv\Scripts\python.exe") {
            Write-Host "✅ Entorno virtual disponible" -ForegroundColor Green
        }
        else {
            Write-Host "❌ Entorno virtual no encontrado" -ForegroundColor Red
        }
    }
    "8" {
        Write-Host "🔄 Sincronizando con GitHub..." -ForegroundColor Magenta
        git add .
        $commitMsg = "🔄 Sync automatico - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        git commit -m $commitMsg
        git push
        git pull
        Write-Host "✅ Sincronizacion completa" -ForegroundColor Green
    }
    "9" {
        Write-Host "📥 Descargando cambios de GitHub..." -ForegroundColor Magenta
        git pull
    }
    "10" {
        Write-Host "📤 Subiendo cambios a GitHub..." -ForegroundColor Magenta
        git add .
        $commitMsg = "📤 Update - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        git commit -m $commitMsg
        git push
    }
    "11" {
        Write-Host "🚀 Iniciando servidor MiloApps..." -ForegroundColor Cyan
        Write-Host "🌐 URL: http://localhost:3000" -ForegroundColor Green
        .venv\Scripts\python.exe src\app.py
    }
    "12" {
        Write-Host "🌐 Abriendo MiloApps en navegador..." -ForegroundColor Cyan
        Start-Process "http://localhost:3000"
    }
    "0" {
        Write-Host "👋 Hasta luego!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "❌ Opcion no valida" -ForegroundColor Red
        Write-Host "Usar numeros del 0 al 12" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✨ Para ejecutar este menu nuevamente:" -ForegroundColor Gray
Write-Host "   powershell -ExecutionPolicy Bypass -File scripts\work-manager-simple.ps1" -ForegroundColor Gray

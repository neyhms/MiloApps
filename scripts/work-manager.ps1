# Script MAESTRO para InfoMilo
# Menú principal para gestionar trabajo desde casa y oficina

Write-Host ""
Write-Host "🚀 INFOMILO - GESTOR DE TRABAJO REMOTO" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Detectar configuración actual
$currentConfig = "desconocida"
if (Test-Path "config\active.json") {
    $config = Get-Content "config\active.json" | ConvertFrom-Json
    $currentConfig = $config.environment
}

Write-Host "📍 Configuración actual: " -NoNewline -ForegroundColor Yellow
switch ($currentConfig) {
    "home" { Write-Host "🏠 CASA" -ForegroundColor Green }
    "office" { Write-Host "🏢 OFICINA" -ForegroundColor Blue }
    default { Write-Host "❓ $currentConfig" -ForegroundColor Gray }
}

Write-Host ""
Write-Host "¿Qué quieres hacer?" -ForegroundColor Cyan
Write-Host ""
Write-Host "🏠 TRABAJO DESDE CASA:" -ForegroundColor Green
Write-Host "  1. Iniciar trabajo en casa" -ForegroundColor White
Write-Host "  2. Terminar trabajo en casa" -ForegroundColor White
Write-Host ""
Write-Host "🏢 TRABAJO DESDE OFICINA:" -ForegroundColor Blue
Write-Host "  3. Iniciar trabajo en oficina" -ForegroundColor White
Write-Host "  4. Terminar trabajo en oficina" -ForegroundColor White
Write-Host ""
Write-Host "⚙️  UTILIDADES:" -ForegroundColor Yellow
Write-Host "  5. Solo cambiar a configuración casa" -ForegroundColor White
Write-Host "  6. Solo cambiar a configuración oficina" -ForegroundColor White
Write-Host "  7. Ver estado del proyecto" -ForegroundColor White
Write-Host ""
Write-Host "🔗 GIT & GITHUB:" -ForegroundColor Magenta
Write-Host "  8. Configurar GitHub (primera vez)" -ForegroundColor White
Write-Host "  9. Sincronizar con GitHub (pull + push)" -ForegroundColor White
Write-Host "  10. Solo descargar cambios (pull)" -ForegroundColor White
Write-Host "  11. Solo subir cambios (push)" -ForegroundColor White
Write-Host ""
Write-Host "  12. Salir" -ForegroundColor White
Write-Host ""

$opcion = Read-Host "Selecciona una opción (1-12)"

switch ($opcion) {
    "1" {
        Write-Host "🏠 Iniciando trabajo desde CASA..." -ForegroundColor Green
        & .\scripts\start-work-home.ps1
    }
    "2" {
        Write-Host "🏠 Terminando trabajo desde CASA..." -ForegroundColor Green
        & .\scripts\end-work-home.ps1
    }
    "3" {
        Write-Host "🏢 Iniciando trabajo desde OFICINA..." -ForegroundColor Blue
        & .\scripts\start-work-office.ps1
    }
    "4" {
        Write-Host "🏢 Terminando trabajo desde OFICINA..." -ForegroundColor Blue
        & .\scripts\end-work-office.ps1
    }
    "5" {
        Write-Host "🏠 Cambiando a configuración de CASA..." -ForegroundColor Yellow
        & .\scripts\switch-env.ps1 home
    }
    "6" {
        Write-Host "🏢 Cambiando a configuración de OFICINA..." -ForegroundColor Yellow
        & .\scripts\switch-env.ps1 office
    }
    "7" {
        Write-Host "📊 ESTADO DEL PROYECTO:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📁 Configuración actual:" -ForegroundColor Yellow
        if (Test-Path "config\active.json") {
            Get-Content "config\active.json" | ConvertFrom-Json | ConvertTo-Json -Depth 3
        }
        Write-Host ""
        Write-Host "📈 Estado de Git:" -ForegroundColor Yellow
        git status
        Write-Host ""
        Write-Host "🐍 Entorno Python:" -ForegroundColor Yellow
        if (Test-Path ".venv\Scripts\python.exe") {
            Write-Host "✅ Entorno virtual disponible" -ForegroundColor Green
            & .venv\Scripts\pip.exe list | Select-String "Flask|python-dotenv|flask-cors"
        } else {
            Write-Host "❌ Entorno virtual no encontrado" -ForegroundColor Red
        }
    }
    "8" {
        Write-Host "� Configurando GitHub primera vez..." -ForegroundColor Magenta
        & .\scripts\setup-github.ps1
    }
    "9" {
        Write-Host "🔄 Sincronizando con GitHub..." -ForegroundColor Magenta
        & .\scripts\git-sync.ps1
    }
    "10" {
        Write-Host "📥 Descargando cambios de GitHub..." -ForegroundColor Magenta
        git pull origin main
    }
    "11" {
        Write-Host "📤 Subiendo cambios a GitHub..." -ForegroundColor Magenta
        & .\scripts\git-push.ps1
    }
    "12" {
        Write-Host "�👋 ¡Hasta luego!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "❌ Opción no válida" -ForegroundColor Red
        Write-Host "Usar: .\scripts\work-manager.ps1" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✨ Para ejecutar este menú nuevamente:" -ForegroundColor Gray
Write-Host "   .\scripts\work-manager.ps1" -ForegroundColor Gray

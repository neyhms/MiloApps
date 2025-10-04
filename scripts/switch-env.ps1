# Script para cambiar entre configuraciones de casa y oficina

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("home", "office", "default")]
    [string]$Environment
)

$configPath = "config/$Environment.json"
$activePath = "config/active.json"

if (!(Test-Path $configPath)) {
    Write-Host "❌ Configuración '$Environment' no encontrada en $configPath" -ForegroundColor Red
    exit 1
}

# Copiar configuración
Copy-Item -Path $configPath -Destination $activePath -Force

# Mostrar mensaje según el entorno
switch ($Environment) {
    "home" {
        Write-Host "🏠 Configurado para trabajo desde CASA" -ForegroundColor Green
        Write-Host "   - Puerto: 3000" -ForegroundColor Gray
        Write-Host "   - Debug: Habilitado" -ForegroundColor Gray
        Write-Host "   - Backup en la nube: Habilitado" -ForegroundColor Gray
    }
    "office" {
        Write-Host "🏢 Configurado para trabajo desde OFICINA" -ForegroundColor Blue
        Write-Host "   - Puerto: 8080" -ForegroundColor Gray
        Write-Host "   - Proxy corporativo: Habilitado" -ForegroundColor Gray
        Write-Host "   - VPN: Requerida" -ForegroundColor Gray
    }
    "default" {
        Write-Host "⚙️  Configuración por defecto activada" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Configuración '$Environment' activada correctamente" -ForegroundColor Green
Write-Host "   Reinicia tu servidor de desarrollo para aplicar los cambios." -ForegroundColor Gray

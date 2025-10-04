# Script para configurar GitHub por primera vez
# Ejecutar este script solo la primera vez para conectar con GitHub

Write-Host "🔗 CONFIGURAR GITHUB - PRIMERA VEZ" -ForegroundColor Magenta
Write-Host "==================================" -ForegroundColor Magenta
Write-Host ""

# Verificar si ya tiene remote configurado
$hasRemote = git remote -v 2>$null
if ($hasRemote) {
    Write-Host "✅ Ya tienes un repositorio remoto configurado:" -ForegroundColor Green
    git remote -v
    Write-Host ""
    $continuar = Read-Host "¿Quieres reconfigurar? (s/N)"
    if ($continuar -ne "s" -and $continuar -ne "S") {
        Write-Host "👍 Manteniendo configuración actual" -ForegroundColor Yellow
        exit 0
    }
    Write-Host "🔄 Eliminando configuración anterior..." -ForegroundColor Yellow
    git remote remove origin 2>$null
}

Write-Host "📋 PASOS PARA CONFIGURAR GITHUB:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣ Crear repositorio en GitHub:" -ForegroundColor Yellow
Write-Host "   • Ir a: https://github.com/new" -ForegroundColor White
Write-Host "   • Nombre: InfoMilo" -ForegroundColor White
Write-Host "   • Privado: ✅ (recomendado)" -ForegroundColor White
Write-Host "   • NO crear README (ya tienes uno)" -ForegroundColor White
Write-Host ""

$confirmar = Read-Host "¿Ya creaste el repositorio en GitHub? (s/N)"
if ($confirmar -ne "s" -and $confirmar -ne "S") {
    Write-Host "👆 Primero crea el repositorio en GitHub y vuelve a ejecutar este script" -ForegroundColor Yellow
    Write-Host "🌐 URL: https://github.com/new" -ForegroundColor Cyan
    exit 0
}

Write-Host ""
Write-Host "2️⃣ Configurar conexión:" -ForegroundColor Yellow

# Pedir el usuario de GitHub
Write-Host ""
$usuario = Read-Host "Ingresa tu usuario de GitHub (ejemplo: neyhms)"
if ([string]::IsNullOrEmpty($usuario)) {
    Write-Host "❌ Usuario requerido" -ForegroundColor Red
    exit 1
}

# Construir URL del repositorio
$repoUrl = "https://github.com/$usuario/InfoMilo.git"
Write-Host ""
Write-Host "🔗 URL del repositorio: $repoUrl" -ForegroundColor Cyan

# Verificar si el usuario quiere continuar
$confirmar = Read-Host "¿Es correcta esta URL? (S/n)"
if ($confirmar -eq "n" -or $confirmar -eq "N") {
    Write-Host "❌ Configuración cancelada" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "⚙️ Configurando repositorio remoto..." -ForegroundColor Yellow

# Agregar remote origin
try {
    git remote add origin $repoUrl
    Write-Host "✅ Remote origin configurado" -ForegroundColor Green
} catch {
    Write-Host "❌ Error configurando remote: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Cambiar branch a main
Write-Host "🔄 Cambiando a branch main..." -ForegroundColor Yellow
try {
    git branch -M main
    Write-Host "✅ Branch main configurado" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Warning al configurar branch main" -ForegroundColor Yellow
}

# Hacer push inicial
Write-Host "📤 Subiendo código a GitHub..." -ForegroundColor Yellow
try {
    git push -u origin main
    Write-Host "✅ Código subido exitosamente a GitHub!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error subiendo a GitHub:" -ForegroundColor Red
    Write-Host "   Posibles causas:" -ForegroundColor Yellow
    Write-Host "   • Repositorio no existe en GitHub" -ForegroundColor Gray
    Write-Host "   • Credenciales incorrectas" -ForegroundColor Gray
    Write-Host "   • Problemas de conexión" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 Verifica en GitHub que el repositorio existe:" -ForegroundColor Cyan
    Write-Host "   $repoUrl" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "🎉 ¡GITHUB CONFIGURADO EXITOSAMENTE!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Configuración guardada:" -ForegroundColor Cyan
Write-Host "   📁 Repositorio: InfoMilo" -ForegroundColor White
Write-Host "   👤 Usuario: $usuario" -ForegroundColor White
Write-Host "   🔗 URL: $repoUrl" -ForegroundColor White
Write-Host "   🌿 Branch: main" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   • En oficina: git clone $repoUrl" -ForegroundColor White
Write-Host "   • Usar script maestro para trabajo diario" -ForegroundColor White
Write-Host "   • Los scripts automáticamente sincronizarán con GitHub" -ForegroundColor White
Write-Host ""

# Guardar configuración para otros scripts
$gitConfig = @{
    repository_url = $repoUrl
    username = $usuario
    configured_date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}
$gitConfig | ConvertTo-Json | Out-File -FilePath "config\git-config.json" -Encoding UTF8
Write-Host "💾 Configuración guardada en config\git-config.json" -ForegroundColor Gray

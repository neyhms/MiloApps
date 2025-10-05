# Script para crear repositorio en GitHub automáticamente
# Usando GitHub CLI o curl

Write-Host "🚀 CREANDO REPOSITORIO MILOAPPS EN GITHUB..." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Datos del repositorio
$repoName = "MiloApps"
$description = "🐱 MiloApps - Sistema de autenticación avanzado con Flask para Milo el gato"
$private = $true

# Verificar si tienes GitHub CLI instalado
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if ($ghInstalled) {
    Write-Host "✅ GitHub CLI encontrado" -ForegroundColor Green
    Write-Host "📦 Creando repositorio con GitHub CLI..." -ForegroundColor Yellow
    
    try {
        if ($private) {
            gh repo create $repoName --description $description --private
        }
        else {
            gh repo create $repoName --description $description --public
        }
        Write-Host "✅ Repositorio creado exitosamente!" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error creando repositorio con GitHub CLI" -ForegroundColor Red
        Write-Host "💡 Probando método alternativo..." -ForegroundColor Yellow
    }
}
else {
    Write-Host "⚠️ GitHub CLI no instalado" -ForegroundColor Yellow
    Write-Host "💡 Intentando crear repositorio manualmente..." -ForegroundColor Yellow
}

# Método alternativo: mostrar instrucciones
Write-Host ""
Write-Host "📋 INSTRUCCIONES PARA CREAR MANUALMENTE:" -ForegroundColor Cyan
Write-Host "1. Ve a: https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: MiloApps" -ForegroundColor White
Write-Host "3. Description: $description" -ForegroundColor White
Write-Host "4. Private: ✅" -ForegroundColor White
Write-Host "5. NO marcar 'Add README' ni 'Add .gitignore'" -ForegroundColor White
Write-Host "6. Click 'Create repository'" -ForegroundColor White
Write-Host ""

# Esperar confirmación
Write-Host "⏳ Esperando 10 segundos para que puedas crear el repo..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Intentar hacer push
Write-Host "📤 Intentando subir código a GitHub..." -ForegroundColor Yellow
try {
    git push -u origin main
    Write-Host "🎉 ¡CÓDIGO SUBIDO EXITOSAMENTE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Tu repositorio: https://github.com/neyhms/MiloApps" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Error al subir código" -ForegroundColor Red
    Write-Host "💡 Asegúrate de haber creado el repositorio en GitHub" -ForegroundColor Yellow
    Write-Host "🔗 https://github.com/new" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🔄 Luego ejecuta: git push -u origin main" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ CONFIGURACIÓN COMPLETA!" -ForegroundColor Green

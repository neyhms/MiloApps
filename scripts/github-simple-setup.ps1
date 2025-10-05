# Script simplificado para configurar GitHub
Write-Host "🔗 CONFIGURANDO GITHUB..." -ForegroundColor Green

# Configurar remote con tu usuario GitHub
$usuario = "neyhms"  # Tu usuario de GitHub
$repoName = "MiloApps"  # Nuevo nombre del repositorio
$repoUrl = "https://github.com/$usuario/$repoName.git"

Write-Host "📁 Repositorio: $repoName" -ForegroundColor Cyan
Write-Host "👤 Usuario: $usuario" -ForegroundColor Cyan
Write-Host "🔗 URL: $repoUrl" -ForegroundColor Cyan
Write-Host ""

# Eliminar remote anterior si existe
git remote remove origin 2>$null

# Configurar nuevo remote
Write-Host "⚙️ Configurando repositorio remoto..." -ForegroundColor Yellow
git remote add origin $repoUrl

# Cambiar a branch main
Write-Host "🔄 Configurando branch main..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "✅ GitHub configurado!" -ForegroundColor Green
Write-Host "📋 Para subir el código:" -ForegroundColor Cyan
Write-Host "   1. Crea el repositorio '$repoName' en GitHub" -ForegroundColor White
Write-Host "   2. Ejecuta: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "🌐 URL para crear repo: https://github.com/new" -ForegroundColor Cyan

# Script para solo subir cambios a GitHub (commit + push)

Write-Host "📤 SUBIR CAMBIOS A GITHUB" -ForegroundColor Magenta
Write-Host "=========================" -ForegroundColor Magenta
Write-Host ""

# Verificar si está en un repositorio git
if (!(Test-Path ".git")) {
    Write-Host "❌ No es un repositorio Git" -ForegroundColor Red
    Write-Host "💡 Ejecuta primero: Opción 8 - Configurar GitHub" -ForegroundColor Yellow
    exit 1
}

# Verificar si tiene remote configurado
$hasRemote = git remote -v 2>$null
if ([string]::IsNullOrEmpty($hasRemote)) {
    Write-Host "❌ No hay repositorio remoto configurado" -ForegroundColor Red
    Write-Host "💡 Ejecuta primero: Opción 8 - Configurar GitHub" -ForegroundColor Yellow
    exit 1
}

# Verificar si hay cambios para subir
Write-Host "🔍 Verificando cambios locales..." -ForegroundColor Yellow
$hasChanges = git status --porcelain 2>$null
if ([string]::IsNullOrEmpty($hasChanges)) {
    Write-Host "✅ No hay cambios para subir" -ForegroundColor Green
    Write-Host "📊 Estado actual:" -ForegroundColor Cyan
    git status --short 2>$null
    
    # Verificar si hay commits para push
    $unpushedCommits = git log origin/main..HEAD --oneline 2>$null
    if ([string]::IsNullOrEmpty($unpushedCommits)) {
        Write-Host "ℹ️ Todo está sincronizado con GitHub" -ForegroundColor Gray
        exit 0
    }
    else {
        Write-Host "📤 Hay commits locales para subir:" -ForegroundColor Yellow
        git log origin/main..HEAD --oneline
        Write-Host ""
        $pushOnly = Read-Host "¿Subir estos commits? (S/n)"
        if ($pushOnly -eq "n" -or $pushOnly -eq "N") {
            exit 0
        }
        # Saltar al push directo
        Write-Host "📤 Subiendo commits existentes..." -ForegroundColor Yellow
        git push origin main
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Commits subidos exitosamente!" -ForegroundColor Green
        }
        exit 0
    }
}

# Mostrar cambios detectados
Write-Host "📝 Cambios detectados:" -ForegroundColor Cyan
git status --short
Write-Host ""

# Preguntar si quiere continuar
$continuar = Read-Host "¿Subir estos cambios a GitHub? (S/n)"
if ($continuar -eq "n" -or $continuar -eq "N") {
    Write-Host "❌ Operación cancelada" -ForegroundColor Yellow
    exit 0
}

# Preguntar por mensaje de commit personalizado
Write-Host ""
Write-Host "💬 Mensaje de commit:" -ForegroundColor Yellow
$mensajeCustom = Read-Host "Presiona Enter para mensaje automático o escribe tu mensaje"

# Agregar cambios al staging
Write-Host ""
Write-Host "📋 Preparando cambios..." -ForegroundColor Yellow
git add .
Write-Host "✅ Cambios agregados" -ForegroundColor Green

# Crear mensaje de commit
if ([string]::IsNullOrWhiteSpace($mensajeCustom)) {
    # Mensaje automático
    $status = git status --porcelain
    $newFiles = ($status | Where-Object { $_ -match "^A " }).Count
    $modifiedFiles = ($status | Where-Object { $_ -match "^M " }).Count
    $deletedFiles = ($status | Where-Object { $_ -match "^D " }).Count
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $location = if (Test-Path "config\active.json") {
        $config = Get-Content "config\active.json" | ConvertFrom-Json
        switch ($config.environment) {
            "home" { "🏠 casa" }
            "office" { "🏢 oficina" }
            default { "💻 local" }
        }
    }
    else { "💻 local" }
    
    $commitMessage = "update: cambios desde $location - $timestamp"
    if ($newFiles -gt 0) { $commitMessage += " (+$newFiles)" }
    if ($modifiedFiles -gt 0) { $commitMessage += " (~$modifiedFiles)" }
    if ($deletedFiles -gt 0) { $commitMessage += " (-$deletedFiles)" }
}
else {
    $commitMessage = $mensajeCustom
}

# Crear commit
Write-Host "💾 Creando commit..." -ForegroundColor Yellow
try {
    git commit -m $commitMessage
    Write-Host "✅ Commit creado: $commitMessage" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error creando commit" -ForegroundColor Red
    exit 1
}

# Subir cambios a GitHub
Write-Host ""
Write-Host "📤 Subiendo a GitHub..." -ForegroundColor Yellow
try {
    git push origin main
    Write-Host "✅ ¡Cambios subidos exitosamente a GitHub!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error subiendo a GitHub" -ForegroundColor Red
    Write-Host "💡 Posibles soluciones:" -ForegroundColor Yellow
    Write-Host "   • Verificar conexión a internet" -ForegroundColor Gray
    Write-Host "   • git pull origin main (si hay conflictos)" -ForegroundColor Gray
    Write-Host "   • Verificar credenciales de GitHub" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "🎉 ¡SUBIDA COMPLETADA!" -ForegroundColor Green
Write-Host "🌐 Tu código está disponible en GitHub ✨" -ForegroundColor Green

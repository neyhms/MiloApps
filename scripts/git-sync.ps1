# Script para sincronizar cambios con GitHub (pull + commit + push)

Write-Host "🔄 SINCRONIZACIÓN CON GITHUB" -ForegroundColor Magenta
Write-Host "============================" -ForegroundColor Magenta
Write-Host ""

# Verificar si está en un repositorio git
if (!(Test-Path ".git")) {
    Write-Host "❌ No es un repositorio Git" -ForegroundColor Red
    Write-Host "💡 Ejecuta primero: Opción 8 - Configurar GitHub" -ForegroundColor Yellow
    exit 1
}

# Verificar si tiene remote configurado
$hasRemote = git remote -v 2>$null
if (![string]::IsNullOrEmpty($hasRemote)) {
    Write-Host "📍 Repositorio remoto:" -ForegroundColor Cyan
    git remote -v | Select-Object -First 1
    Write-Host ""
}
else {
    Write-Host "❌ No hay repositorio remoto configurado" -ForegroundColor Red
    Write-Host "💡 Ejecuta primero: Opción 8 - Configurar GitHub" -ForegroundColor Yellow
    exit 1
}

# Paso 1: Descargar cambios del remoto
Write-Host "📥 1. Descargando cambios de GitHub..." -ForegroundColor Yellow
try {
    $pullResult = git pull origin main 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Cambios descargados exitosamente" -ForegroundColor Green
        if ($pullResult -match "Already up to date") {
            Write-Host "   ℹ️ Ya estás actualizado" -ForegroundColor Gray
        }
    }
    else {
        Write-Host "⚠️ Posibles conflictos al descargar:" -ForegroundColor Yellow
        Write-Host $pullResult -ForegroundColor Gray
        Write-Host ""
        Write-Host "🔧 Resolviendo automáticamente..." -ForegroundColor Yellow
        # Intentar merge automático
        git merge --no-edit 2>$null
    }
}
catch {
    Write-Host "❌ Error descargando cambios" -ForegroundColor Red
    Write-Host "💡 Verifica tu conexión a internet" -ForegroundColor Yellow
}

Write-Host ""

# Paso 2: Verificar si hay cambios locales
Write-Host "🔍 2. Verificando cambios locales..." -ForegroundColor Yellow
$hasChanges = git status --porcelain 2>$null
if ([string]::IsNullOrEmpty($hasChanges)) {
    Write-Host "✅ No hay cambios para subir" -ForegroundColor Green
    Write-Host "📊 Estado actual:" -ForegroundColor Cyan
    git status --short 2>$null
    exit 0
}

# Mostrar cambios detectados
Write-Host "📝 Cambios detectados:" -ForegroundColor Cyan
git status --short

Write-Host ""

# Paso 3: Agregar cambios al staging
Write-Host "📋 3. Preparando cambios..." -ForegroundColor Yellow
git add .
Write-Host "✅ Cambios agregados al staging" -ForegroundColor Green

Write-Host ""

# Paso 4: Crear commit automático
Write-Host "💾 4. Creando commit..." -ForegroundColor Yellow

# Detectar tipo de cambios para mensaje automático
$status = git status --porcelain
$newFiles = ($status | Where-Object { $_ -match "^A " }).Count
$modifiedFiles = ($status | Where-Object { $_ -match "^M " }).Count
$deletedFiles = ($status | Where-Object { $_ -match "^D " }).Count

# Generar mensaje de commit automático
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$location = if (Test-Path "config\active.json") {
    $config = Get-Content "config\active.json" | ConvertFrom-Json
    switch ($config.environment) {
        "home" { "🏠 casa" }
        "office" { "🏢 oficina" }
        default { "💻 ubicación" }
    }
}
else { "💻 local" }

$commitMessage = "chore: sync from $location - $timestamp"
if ($newFiles -gt 0) { $commitMessage += " (+$newFiles nuevos)" }
if ($modifiedFiles -gt 0) { $commitMessage += " (~$modifiedFiles modificados)" }
if ($deletedFiles -gt 0) { $commitMessage += " (-$deletedFiles eliminados)" }

try {
    git commit -m $commitMessage
    Write-Host "✅ Commit creado: $commitMessage" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error creando commit" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Paso 5: Subir cambios a GitHub
Write-Host "📤 5. Subiendo cambios a GitHub..." -ForegroundColor Yellow
try {
    git push origin main
    Write-Host "✅ Cambios subidos exitosamente a GitHub!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error subiendo a GitHub" -ForegroundColor Red
    Write-Host "💡 Posibles causas:" -ForegroundColor Yellow
    Write-Host "   • Problemas de conexión" -ForegroundColor Gray
    Write-Host "   • Credenciales incorrectas" -ForegroundColor Gray
    Write-Host "   • Conflictos en el repositorio" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "🎉 ¡SINCRONIZACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Resumen:" -ForegroundColor Cyan
Write-Host "   📁 Archivos nuevos: $newFiles" -ForegroundColor White
Write-Host "   📝 Archivos modificados: $modifiedFiles" -ForegroundColor White
Write-Host "   🗑️ Archivos eliminados: $deletedFiles" -ForegroundColor White
Write-Host "   📍 Desde: $location" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Tu código está sincronizado en GitHub ✨" -ForegroundColor Green

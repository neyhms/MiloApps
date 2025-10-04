# Script para INICIAR trabajo desde CASA
# Ejecutar al comenzar el día de trabajo en casa

Write-Host "🏠 INICIANDO TRABAJO DESDE CASA..." -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Paso 1: Sincronizar cambios desde GitHub
Write-Host "📥 1. Sincronizando cambios desde GitHub..." -ForegroundColor Yellow
if (Test-Path ".git") {
    $hasRemote = git remote -v 2>$null
    if (![string]::IsNullOrEmpty($hasRemote)) {
        try {
            $pullResult = git pull origin main 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Cambios sincronizados desde GitHub" -ForegroundColor Green
                if ($pullResult -match "Already up to date") {
                    Write-Host "   ℹ️ Ya tienes la versión más reciente" -ForegroundColor Gray
                } else {
                    Write-Host "   📦 Cambios aplicados desde oficina" -ForegroundColor Cyan
                }
            } else {
                Write-Host "⚠️ Posibles conflictos - revisar manualmente" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "⚠️ Error de conexión - continuando sin sincronizar" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️ GitHub no configurado - usar opción 8 del menú principal" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️ No es repositorio Git - usar opción 8 para configurar GitHub" -ForegroundColor Yellow
}

# Paso 2: Configurar para casa
Write-Host "🏠 2. Configurando entorno de CASA..." -ForegroundColor Yellow
Copy-Item -Path "config\home.json" -Destination "config\active.json" -Force

# Verificar configuración
$config = Get-Content "config\active.json" | ConvertFrom-Json
if ($config.environment -eq "home") {
    Write-Host "✅ Configuración de CASA activada" -ForegroundColor Green
} else {
    Write-Host "❌ Error en configuración" -ForegroundColor Red
}

# Paso 3: Configurar Git personal
Write-Host "👤 3. Configurando Git personal..." -ForegroundColor Yellow
$currentEmail = git config user.email 2>$null
if ($currentEmail -notlike "*personal*" -and $currentEmail -notlike "*gmail*") {
    Write-Host "   💡 Tip: Configurar email personal con:" -ForegroundColor Gray
    Write-Host "   git config user.email tu.email@personal.com" -ForegroundColor Gray
}

# Paso 4: Preparar entorno Python
Write-Host "🐍 4. Preparando entorno Python..." -ForegroundColor Yellow
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "✅ Entorno virtual encontrado" -ForegroundColor Green
} else {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    & .venv\Scripts\pip.exe install -r requirements.txt
}

# Paso 5: Iniciar aplicación automáticamente
Write-Host "🚀 5. Iniciando aplicación Flask..." -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 ¡CASA CONFIGURADA!" -ForegroundColor Green
Write-Host "📋 INFORMACIÓN:" -ForegroundColor Cyan
Write-Host "   🌐 URL: http://localhost:3000" -ForegroundColor White
Write-Host "   🏠 Entorno: CASA" -ForegroundColor White
Write-Host "   🐛 Debug: HABILITADO" -ForegroundColor White
Write-Host "   ☁️  Backup: Cloud sync" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Iniciando servidor..." -ForegroundColor Green

# Activar entorno e iniciar
& .venv\Scripts\activate
Start-Process "http://localhost:3000"
& .venv\Scripts\python.exe src\app.py

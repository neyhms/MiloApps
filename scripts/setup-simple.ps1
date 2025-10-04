# InfoMilo Setup Script
param([string]$Environment = "default")

Write-Host "Configurando InfoMilo para trabajo remoto..." -ForegroundColor Green

# Verificar Node.js
try {
    $nodeVersion = node --version 2>$null
    Write-Host "Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Node.js no encontrado" -ForegroundColor Red
    exit 1
}

# Crear directorios
$directories = @("temp", "logs", "dist", "build")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Creado directorio: $dir" -ForegroundColor Yellow
    }
}

# Configuración activa
$configFile = "config/$Environment.json"
if (Test-Path $configFile) {
    Copy-Item -Path $configFile -Destination "config/active.json" -Force
    Write-Host "Configuracion '$Environment' activada" -ForegroundColor Cyan
} else {
    Copy-Item -Path "config/default.json" -Destination "config/active.json" -Force
    Write-Host "Usando configuracion por defecto" -ForegroundColor Cyan
}

# Crear .env
if (!(Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host "Archivo .env creado" -ForegroundColor Yellow
    }
}

# Instalar dependencias
if (Test-Path "package.json") {
    Write-Host "Instalando dependencias..." -ForegroundColor Cyan
    npm install
}

Write-Host ""
Write-Host "Configuracion completada!" -ForegroundColor Green
Write-Host "Comandos disponibles:" -ForegroundColor Cyan
Write-Host "  - npm run dev (iniciar desarrollo)" -ForegroundColor White
Write-Host "  - npm run build (construir proyecto)" -ForegroundColor White

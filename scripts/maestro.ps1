#!/usr/bin/env powershell
# Script MAESTRO para MiloApps - Version funcional
# Menu principal para gestionar trabajo desde casa y oficina

param([string]$Opcion)

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "🐱 MILOAPPS - GESTOR DE TRABAJO REMOTO" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host ""

    # Detectar configuracion actual
    $currentConfig = "desconocida"
    if (Test-Path "config\active.json") {
        try {
            $config = Get-Content "config\active.json" | ConvertFrom-Json
            $currentConfig = $config.environment
        }
        catch {
            $currentConfig = "error"
        }
    }

    Write-Host "📍 Configuracion actual: " -NoNewline -ForegroundColor Yellow
    switch ($currentConfig) {
        "home" { Write-Host "🏠 CASA" -ForegroundColor Green }
        "office" { Write-Host "🏢 OFICINA" -ForegroundColor Blue }
        default { Write-Host "❓ $currentConfig" -ForegroundColor Gray }
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
    Write-Host "  8. Sincronizar con GitHub (pull + push)" -ForegroundColor White
    Write-Host "  9. Solo descargar cambios (pull)" -ForegroundColor White
    Write-Host "  10. Solo subir cambios (push)" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 MILOAPPS:" -ForegroundColor Cyan
    Write-Host "  11. Iniciar servidor MiloApps" -ForegroundColor White
    Write-Host "  12. Abrir MiloApps en navegador" -ForegroundColor White
    Write-Host ""
    Write-Host "  0. Salir" -ForegroundColor White
    Write-Host ""
}

function Execute-Option {
    param([string]$Option)
    
    switch ($Option) {
        "1" {
            Write-Host "🏠 Iniciando trabajo desde CASA..." -ForegroundColor Green
            # Cambiar a configuracion casa
            Copy-Item -Path "config\home.json" -Destination "config\active.json" -Force
            Write-Host "✅ Configuracion de CASA activada" -ForegroundColor Green
            
            # Sincronizar desde GitHub
            Write-Host "📥 Sincronizando desde GitHub..." -ForegroundColor Yellow
            if (Test-Path ".git") {
                git pull 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Cambios sincronizados" -ForegroundColor Green
                }
            }
            
            Write-Host "🚀 Listo para trabajar desde casa!" -ForegroundColor Green
            Write-Host "🌐 URL: http://localhost:3000" -ForegroundColor Cyan
        }
        
        "2" {
            Write-Host "🏠 Terminando trabajo desde CASA..." -ForegroundColor Green
            # Sync automatico
            git add . 2>$null
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
            git commit -m "🏠 Fin trabajo casa - $timestamp" 2>$null
            git push 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Cambios guardados en GitHub" -ForegroundColor Green
            }
            Write-Host "👋 Trabajo en casa terminado!" -ForegroundColor Green
        }
        
        "3" {
            Write-Host "🏢 Iniciando trabajo desde OFICINA..." -ForegroundColor Blue
            # Cambiar a configuracion oficina
            Copy-Item -Path "config\office.json" -Destination "config\active.json" -Force
            Write-Host "✅ Configuracion de OFICINA activada" -ForegroundColor Blue
            Write-Host "🌐 URL: http://localhost:8080" -ForegroundColor Cyan
        }
        
        "4" {
            Write-Host "🏢 Terminando trabajo desde OFICINA..." -ForegroundColor Blue
            # Sync automatico
            git add . 2>$null
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
            git commit -m "🏢 Fin trabajo oficina - $timestamp" 2>$null
            git push 2>$null
            Write-Host "👋 Trabajo en oficina terminado!" -ForegroundColor Blue
        }
        
        "5" {
            Write-Host "🏠 Cambiando a configuracion de CASA..." -ForegroundColor Yellow
            Copy-Item -Path "config\home.json" -Destination "config\active.json" -Force
            Write-Host "✅ Configuracion de CASA activada" -ForegroundColor Green
        }
        
        "6" {
            Write-Host "🏢 Cambiando a configuracion de OFICINA..." -ForegroundColor Yellow
            Copy-Item -Path "config\office.json" -Destination "config\active.json" -Force
            Write-Host "✅ Configuracion de OFICINA activada" -ForegroundColor Blue
        }
        
        "7" {
            Write-Host "📊 ESTADO DEL PROYECTO:" -ForegroundColor Cyan
            Write-Host ""
            
            # Configuracion
            Write-Host "📁 Configuracion:" -ForegroundColor Yellow
            if (Test-Path "config\active.json") {
                $config = Get-Content "config\active.json" | ConvertFrom-Json
                Write-Host "   Entorno: $($config.environment)" -ForegroundColor White
                Write-Host "   Puerto: $($config.development.port)" -ForegroundColor White
                Write-Host "   Debug: $($config.development.debug_mode)" -ForegroundColor White
            }
            
            Write-Host ""
            Write-Host "📈 Git:" -ForegroundColor Yellow
            $gitStatus = git status --porcelain 2>$null
            if ($gitStatus) {
                Write-Host "   ⚠️ Hay cambios sin commitear" -ForegroundColor Yellow
            }
            else {
                Write-Host "   ✅ Todo commiteado" -ForegroundColor Green
            }
            
            Write-Host ""
            Write-Host "🐍 Python:" -ForegroundColor Yellow
            if (Test-Path ".venv\Scripts\python.exe") {
                Write-Host "   ✅ Entorno virtual OK" -ForegroundColor Green
            }
            else {
                Write-Host "   ❌ Problema con entorno" -ForegroundColor Red
            }
        }
        
        "8" {
            Write-Host "🔄 Sincronizando con GitHub..." -ForegroundColor Magenta
            git add . 2>$null
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
            git commit -m "🔄 Sync - $timestamp" 2>$null
            git push 2>$null
            git pull 2>$null
            Write-Host "✅ Sincronizacion completa" -ForegroundColor Green
        }
        
        "9" {
            Write-Host "📥 Descargando cambios..." -ForegroundColor Magenta
            git pull
            Write-Host "✅ Cambios descargados" -ForegroundColor Green
        }
        
        "10" {
            Write-Host "📤 Subiendo cambios..." -ForegroundColor Magenta
            git add .
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
            git commit -m "📤 Update - $timestamp"
            git push
            Write-Host "✅ Cambios subidos" -ForegroundColor Green
        }
        
        "11" {
            Write-Host "🚀 Iniciando servidor MiloApps..." -ForegroundColor Cyan
            $config = Get-Content "config\active.json" | ConvertFrom-Json
            $port = $config.development.port
            Write-Host "🌐 URL: http://localhost:$port" -ForegroundColor Green
            Write-Host "🔑 Admin: admin@miloapps.com / MiloAdmin2024!" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Gray
            & .venv\Scripts\python.exe src\app.py
        }
        
        "12" {
            Write-Host "🌐 Abriendo MiloApps..." -ForegroundColor Cyan
            $config = Get-Content "config\active.json" | ConvertFrom-Json
            $port = $config.development.port
            Start-Process "http://localhost:$port"
            Write-Host "✅ Navegador abierto" -ForegroundColor Green
        }
        
        "0" {
            Write-Host "👋 Hasta luego!" -ForegroundColor Green
            exit 0
        }
        
        default {
            Write-Host "❌ Opcion no valida. Usa numeros del 0 al 12" -ForegroundColor Red
        }
    }
}

# Ejecucion principal
if ($Opcion) {
    Execute-Option -Option $Opcion
}
else {
    Show-Menu
    $userChoice = Read-Host "Selecciona una opcion (0-12)"
    Execute-Option -Option $userChoice
}

Write-Host ""
Write-Host "✨ Para ejecutar nuevamente:" -ForegroundColor Gray
Write-Host "   .\scripts\maestro.ps1" -ForegroundColor Gray
Write-Host ""

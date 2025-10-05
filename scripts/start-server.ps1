# InfoMilo Web Server - PowerShell Version
# Servidor web básico para cuando Node.js no está disponible

param(
    [int]$Port = 8080
)

# Cargar configuración activa
$configPath = "config/active.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    $Port = $config.development.port
    Write-Host "🚀 Iniciando InfoMilo Server..." -ForegroundColor Green
    Write-Host "📋 Configuración: $($config.environment.ToUpper())" -ForegroundColor Cyan
}
else {
    Write-Host "⚠️  Usando configuración por defecto" -ForegroundColor Yellow
}

# Crear el listener HTTP
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()

Write-Host "✅ Servidor iniciado correctamente!" -ForegroundColor Green
Write-Host "🌐 URL: http://localhost:$Port" -ForegroundColor White
Write-Host "📄 Endpoints disponibles:" -ForegroundColor Cyan
Write-Host "   - http://localhost:$Port/" -ForegroundColor Gray
Write-Host "   - http://localhost:$Port/config" -ForegroundColor Gray
Write-Host "   - http://localhost:$Port/status" -ForegroundColor Gray
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Función para generar HTML de la página principal
function Get-HomePage {
    param($config)
    
    $environment = if ($config) { $config.environment } else { "default" }
    $environmentEmoji = switch ($environment) {
        "home" { "🏠" }
        "office" { "🏢" }
        default { "⚙️" }
    }
    
    return @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InfoMilo - Trabajo Remoto Flexible</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            width: 90%;
        }
        h1 { 
            font-size: 2.5em; 
            margin-bottom: 20px;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .status {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .environment {
            font-size: 1.5em;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .info-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .links a {
            color: #fff;
            text-decoration: none;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 25px;
            margin: 0 10px;
            display: inline-block;
            margin-bottom: 10px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .links a:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        .footer {
            margin-top: 30px;
            font-size: 0.9em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 InfoMilo</h1>
        <p>Proyecto flexible para trabajo remoto</p>
        
        <div class="status">
            <div class="environment">
                $environmentEmoji $($environment.ToUpper())
            </div>
            <p>Servidor PowerShell - Funciona sin Node.js</p>
        </div>

        <div class="info-item">
            <strong>🌐 Puerto:</strong> $Port
        </div>
        
        <div class="info-item">
            <strong>💻 Servidor:</strong> PowerShell HTTP Listener
        </div>

        <div class="links">
            <h3>🔗 Enlaces</h3>
            <a href="/config">⚙️ Configuración</a>
            <a href="/status">📊 Estado</a>
        </div>

        <div class="footer">
            <p>💡 Para cambiar configuración:</p>
            <p><code>.\scripts\switch-env.ps1 home</code> o <code>.\scripts\switch-env.ps1 office</code></p>
            <small>$(Get-Date)</small>
        </div>
    </div>
</body>
</html>
"@
}

# Loop principal del servidor
try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $url = $request.Url.AbsolutePath
        
        # Configurar headers
        $response.Headers.Add("Access-Control-Allow-Origin", "*")
        $response.ContentType = "text/html; charset=utf-8"
        
        # Router básico
        switch ($url) {
            "/" {
                $html = Get-HomePage -config $config
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($html)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
            "/config" {
                $response.ContentType = "application/json; charset=utf-8"
                if ($config) {
                    $json = $config | ConvertTo-Json -Depth 10
                }
                else {
                    $json = '{"environment": "default", "note": "No config loaded"}'
                }
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($json)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
            "/status" {
                $response.ContentType = "application/json; charset=utf-8"
                $status = @{
                    status    = "running"
                    server    = "PowerShell"
                    port      = $Port
                    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                } | ConvertTo-Json
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($status)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
            default {
                $response.StatusCode = 404
                $html = "<h1>404 - Página no encontrada</h1><p><a href='/'>Volver al inicio</a></p>"
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($html)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
        }
        
        $response.Close()
        Write-Host "$(Get-Date -Format 'HH:mm:ss') - $($request.HttpMethod) $url" -ForegroundColor Gray
    }
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
finally {
    $listener.Stop()
    Write-Host "📴 Servidor detenido" -ForegroundColor Yellow
}

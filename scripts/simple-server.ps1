# Servidor web simple para InfoMilo
param([int]$Port = 8080)

# Crear página HTML simple
$html = @"
<!DOCTYPE html>
<html>
<head>
    <title>InfoMilo - Trabajo Remoto</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f0f2f5; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #1976d2; text-align: center; }
        .status { background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .links { text-align: center; margin: 30px 0; }
        .links a { display: inline-block; margin: 10px; padding: 10px 20px; background: #1976d2; color: white; text-decoration: none; border-radius: 5px; }
        .info { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 InfoMilo</h1>
        <p style="text-align: center;">Proyecto flexible para trabajo remoto</p>
        
        <div class="status">
            <h3>✅ Servidor Activo</h3>
            <p>Puerto: $Port | Servidor: PowerShell</p>
        </div>

        <div class="info">
            <strong>🏠 Configuraciones disponibles:</strong>
            <ul>
                <li>Casa: Optimizada para trabajo desde hogar</li>
                <li>Oficina: Configurada para entorno corporativo</li>
                <li>Default: Configuración genérica</li>
            </ul>
        </div>

        <div class="links">
            <a href="/config">⚙️ Ver Configuración</a>
            <a href="/status">📊 Estado del Sistema</a>
        </div>

        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>💡 Para cambiar configuración usa:</p>
            <code>.\scripts\switch-env.ps1 home</code> o <code>.\scripts\switch-env.ps1 office</code>
        </div>
    </div>
</body>
</html>
"@

Write-Host "🚀 Iniciando InfoMilo Server..." -ForegroundColor Green
Write-Host "🌐 URL: http://localhost:$Port" -ForegroundColor Cyan

# Iniciar servidor HTTP simple
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()

Write-Host "✅ Servidor iniciado! Presiona Ctrl+C para detener" -ForegroundColor Green

try {
    while ($true) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $url = $request.Url.AbsolutePath
        
        switch ($url) {
            "/" {
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($html)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
            "/config" {
                $response.ContentType = "application/json"
                $json = '{"environment": "default", "port": ' + $Port + ', "server": "PowerShell"}'
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($json)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
            "/status" {
                $response.ContentType = "application/json"
                $json = '{"status": "running", "timestamp": "' + (Get-Date) + '"}'
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($json)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
            default {
                $response.StatusCode = 404
                $notfound = "<h1>404 - No encontrado</h1><a href='/'>Volver</a>"
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($notfound)
                $response.ContentLength64 = $buffer.Length
                $response.OutputStream.Write($buffer, 0, $buffer.Length)
            }
        }
        
        $response.Close()
        Write-Host "$(Get-Date -Format 'HH:mm:ss') - $($request.HttpMethod) $url"
    }
}
finally {
    $listener.Stop()
    Write-Host "📴 Servidor detenido" -ForegroundColor Yellow
}

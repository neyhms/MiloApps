// InfoMilo - Aplicación Principal
// Proyecto flexible para trabajo remoto

const fs = require('fs');
const path = require('path');

class InfoMiloApp {
    constructor() {
        this.config = this.loadConfig();
        this.init();
    }

    loadConfig() {
        try {
            // Intentar cargar configuración activa
            const activeConfigPath = path.join(__dirname, '../config/active.json');
            if (fs.existsSync(activeConfigPath)) {
                const config = JSON.parse(fs.readFileSync(activeConfigPath, 'utf8'));
                console.log(`📋 Configuración cargada: ${config.environment.toUpperCase()}`);
                return config;
            }
        } catch (error) {
            console.log('⚠️  Error cargando configuración activa, usando default');
        }

        // Cargar configuración por defecto
        try {
            const defaultConfigPath = path.join(__dirname, '../config/default.json');
            const config = JSON.parse(fs.readFileSync(defaultConfigPath, 'utf8'));
            console.log('📋 Usando configuración por defecto');
            return config;
        } catch (error) {
            console.error('❌ Error cargando configuración:', error.message);
            process.exit(1);
        }
    }

    init() {
        console.log('🚀 Iniciando InfoMilo...');
        console.log(`📍 Entorno: ${this.config.environment}`);
        console.log(`🌐 Puerto: ${this.config.development.port}`);
        console.log(`🏠 Host: ${this.config.development.host}`);
        
        if (this.config.network.proxy) {
            console.log(`🔗 Proxy: ${this.config.network.proxy_url || 'Configurado'}`);
        }
        
        if (this.config.development.debug_mode) {
            console.log('🐛 Modo debug: ACTIVADO');
        }

        this.startServer();
    }

    startServer() {
        const http = require('http');
        
        const server = http.createServer((req, res) => {
            // Configurar CORS básico
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
            res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

            // Router básico
            if (req.url === '/') {
                res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end(this.getHomePage());
            } else if (req.url === '/api/config') {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(this.config, null, 2));
            } else if (req.url === '/api/status') {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    status: 'running',
                    environment: this.config.environment,
                    timestamp: new Date().toISOString(),
                    uptime: process.uptime()
                }));
            } else {
                res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end('<h1>404 - Página no encontrada</h1>');
            }
        });

        server.listen(this.config.development.port, this.config.development.host, () => {
            console.log('');
            console.log('✅ Servidor iniciado correctamente!');
            console.log(`🌐 URL: http://${this.config.development.host}:${this.config.development.port}`);
            console.log('');
            console.log('Endpoints disponibles:');
            console.log(`   📄 Home: http://${this.config.development.host}:${this.config.development.port}/`);
            console.log(`   ⚙️  Config: http://${this.config.development.host}:${this.config.development.port}/api/config`);
            console.log(`   📊 Status: http://${this.config.development.host}:${this.config.development.port}/api/status`);
            console.log('');
            console.log('Para cambiar configuración:');
            console.log('   🏠 Casa: npm run switch:home');
            console.log('   🏢 Oficina: npm run switch:office');
            console.log('');
        });

        // Manejo graceful de cierre
        process.on('SIGINT', () => {
            console.log('\n📴 Cerrando servidor...');
            server.close(() => {
                console.log('✅ Servidor cerrado correctamente');
                process.exit(0);
            });
        });
    }

    getHomePage() {
        const environment = this.config.environment;
        const environmentEmoji = environment === 'home' ? '🏠' : environment === 'office' ? '🏢' : '⚙️';
        
        return `
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
                .info-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }
                .info-item {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                .api-links {
                    margin-top: 30px;
                }
                .api-links a {
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
                .api-links a:hover {
                    background: rgba(255, 255, 255, 0.3);
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                }
                .footer {
                    margin-top: 30px;
                    font-size: 0.9em;
                    opacity: 0.8;
                }
                @media (max-width: 600px) {
                    h1 { font-size: 2em; }
                    .container { padding: 20px; }
                    .info-grid { grid-template-columns: 1fr; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 InfoMilo</h1>
                <p>Proyecto flexible para trabajo remoto</p>
                
                <div class="status">
                    <div class="environment">
                        ${environmentEmoji} ${environment.toUpperCase()}
                    </div>
                    <p>${this.config.description}</p>
                </div>

                <div class="info-grid">
                    <div class="info-item">
                        <strong>🌐 Puerto</strong><br>
                        ${this.config.development.port}
                    </div>
                    <div class="info-item">
                        <strong>🏠 Host</strong><br>
                        ${this.config.development.host}
                    </div>
                    <div class="info-item">
                        <strong>🔗 Proxy</strong><br>
                        ${this.config.network.proxy ? 'Habilitado' : 'Deshabilitado'}
                    </div>
                    <div class="info-item">
                        <strong>🐛 Debug</strong><br>
                        ${this.config.development.debug_mode ? 'Activo' : 'Inactivo'}
                    </div>
                </div>

                <div class="api-links">
                    <h3>🔗 Enlaces de API</h3>
                    <a href="/api/config">⚙️ Configuración</a>
                    <a href="/api/status">📊 Estado</a>
                </div>

                <div class="footer">
                    <p>💡 Para cambiar configuración, usa los scripts en la terminal</p>
                    <small>Timestamp: ${new Date().toLocaleString()}</small>
                </div>
            </div>
        </body>
        </html>
        `;
    }
}

// Iniciar la aplicación
if (require.main === module) {
    new InfoMiloApp();
}

module.exports = InfoMiloApp;

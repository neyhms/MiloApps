// Build script para InfoMilo

const fs = require('fs');
const path = require('path');

console.log('🔨 Iniciando build de InfoMilo...');

// Crear directorio dist si no existe
const distDir = path.join(__dirname, '../dist');
if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
    console.log('📁 Directorio dist creado');
}

// Copiar archivos necesarios
const filesToCopy = [
    { src: 'src/index.js', dest: 'dist/index.js' },
    { src: 'package.json', dest: 'dist/package.json' }
];

filesToCopy.forEach(file => {
    const srcPath = path.join(__dirname, '..', file.src);
    const destPath = path.join(__dirname, '..', file.dest);
    
    if (fs.existsSync(srcPath)) {
        fs.copyFileSync(srcPath, destPath);
        console.log(`✅ Copiado: ${file.src} -> ${file.dest}`);
    } else {
        console.log(`⚠️  Archivo no encontrado: ${file.src}`);
    }
});

// Crear archivo de información de build
const buildInfo = {
    version: require('../package.json').version,
    buildDate: new Date().toISOString(),
    nodeVersion: process.version,
    platform: process.platform
};

fs.writeFileSync(
    path.join(distDir, 'build-info.json'),
    JSON.stringify(buildInfo, null, 2)
);

console.log('📦 Build completado exitosamente!');
console.log(`📅 Fecha: ${buildInfo.buildDate}`);
console.log(`📋 Versión: ${buildInfo.version}`);
console.log('🎉 Archivos listos en la carpeta dist/');

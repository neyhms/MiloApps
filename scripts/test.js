// Test script básico para InfoMilo

console.log('🧪 Ejecutando tests de InfoMilo...');

// Mock de tests básicos
const tests = [
    {
        name: 'Configuración por defecto',
        test: () => {
            const fs = require('fs');
            const path = require('path');
            const configPath = path.join(__dirname, '../config/default.json');
            return fs.existsSync(configPath);
        }
    },
    {
        name: 'Configuración de casa',
        test: () => {
            const fs = require('fs');
            const path = require('path');
            const configPath = path.join(__dirname, '../config/home.json');
            return fs.existsSync(configPath);
        }
    },
    {
        name: 'Configuración de oficina',
        test: () => {
            const fs = require('fs');
            const path = require('path');
            const configPath = path.join(__dirname, '../config/office.json');
            return fs.existsSync(configPath);
        }
    },
    {
        name: 'Archivo principal existe',
        test: () => {
            const fs = require('fs');
            const path = require('path');
            const mainPath = path.join(__dirname, '../src/index.js');
            return fs.existsSync(mainPath);
        }
    },
    {
        name: 'Package.json válido',
        test: () => {
            try {
                const pkg = require('../package.json');
                return pkg.name && pkg.version && pkg.scripts;
            } catch {
                return false;
            }
        }
    }
];

let passed = 0;
let failed = 0;

console.log('');
tests.forEach((test, index) => {
    try {
        const result = test.test();
        if (result) {
            console.log(`✅ Test ${index + 1}: ${test.name}`);
            passed++;
        } else {
            console.log(`❌ Test ${index + 1}: ${test.name}`);
            failed++;
        }
    } catch (error) {
        console.log(`❌ Test ${index + 1}: ${test.name} - Error: ${error.message}`);
        failed++;
    }
});

console.log('');
console.log('📊 Resultados:');
console.log(`   ✅ Pasados: ${passed}`);
console.log(`   ❌ Fallidos: ${failed}`);
console.log(`   📈 Total: ${tests.length}`);

if (failed === 0) {
    console.log('🎉 ¡Todos los tests pasaron!');
    process.exit(0);
} else {
    console.log('💥 Algunos tests fallaron');
    process.exit(1);
}

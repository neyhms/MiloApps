# Guía de Desarrollo - InfoMilo

Esta guía cubre las mejores prácticas para desarrollar en el proyecto InfoMilo, optimizado para trabajo remoto.

## 🏗️ Arquitectura del Proyecto

### Estructura Modular
```
src/
├── components/          # Componentes reutilizables
├── services/           # Lógica de negocio
├── utils/              # Utilidades y helpers
├── config/             # Configuraciones de app
└── tests/              # Tests unitarios
```

### Principios de Diseño
- **Modularidad**: Componentes independientes y reutilizables
- **Separación de responsabilidades**: Cada módulo tiene una función específica
- **Configurabilidad**: Adaptable a diferentes entornos
- **Testabilidad**: Código fácil de probar

## 🔄 Flujo de Trabajo

### Desarrollo Diario
1. **Sincronizar código**
   ```bash
   git pull origin main
   ```

2. **Cambiar entorno según ubicación**
   ```powershell
   # En casa
   .\scripts\switch-env.ps1 home
   
   # En oficina
   .\scripts\switch-env.ps1 office
   ```

3. **Iniciar servidor de desarrollo**
   ```bash
   npm run dev
   ```

4. **Desarrollar con hot reload habilitado**

### Crear Nueva Funcionalidad
1. **Crear branch**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Desarrollar y testear**
   ```bash
   npm run test
   npm run build
   ```

3. **Commit y push**
   ```bash
   git add .
   git commit -m "feat: agregar nueva funcionalidad"
   git push origin feature/nueva-funcionalidad
   ```

4. **Crear Pull Request**

## 🧪 Testing

### Estrategia de Testing
- **Unit Tests**: Para funciones y componentes individuales
- **Integration Tests**: Para flujos completos
- **E2E Tests**: Para casos de usuario críticos

### Comandos de Testing
```bash
# Ejecutar todos los tests
npm test

# Tests en modo watch
npm run test:watch

# Coverage report
npm run test:coverage

# Tests específicos
npm test -- --grep "component"
```

### Escribir Tests
```javascript
// Ejemplo de test unitario
describe('UtilityFunction', () => {
  it('should return expected result', () => {
    const result = utilityFunction('input');
    expect(result).toBe('expected');
  });
});
```

## 📝 Convenciones de Código

### Naming Conventions
```javascript
// Variables y funciones: camelCase
const userName = 'john';
function getUserData() {}

// Constantes: UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.example.com';

// Clases: PascalCase
class UserService {}

// Archivos: kebab-case
user-service.js
api-client.js
```

### Estructura de Archivos
```javascript
// 1. Imports
import React from 'react';
import { useState } from 'react';

// 2. Constants
const DEFAULT_OPTIONS = {};

// 3. Main component/function
function MyComponent() {
  // 3.1 State
  const [state, setState] = useState();
  
  // 3.2 Effects
  useEffect(() => {}, []);
  
  // 3.3 Event handlers
  const handleClick = () => {};
  
  // 3.4 Render
  return <div></div>;
}

// 4. Export
export default MyComponent;
```

### Comentarios
```javascript
/**
 * Calcula el precio total incluyendo impuestos
 * @param {number} basePrice - Precio base del producto
 * @param {number} taxRate - Tasa de impuesto (0.1 = 10%)
 * @returns {number} Precio total con impuestos
 */
function calculateTotalPrice(basePrice, taxRate) {
  // Aplicar tasa de impuesto
  const tax = basePrice * taxRate;
  return basePrice + tax;
}
```

## 🚀 Build y Deploy

### Proceso de Build
```bash
# Development build
npm run build:dev

# Production build
npm run build:prod

# Análisis del bundle
npm run analyze
```

### Proceso de Deploy
```bash
# Deploy a staging
.\scripts\deploy.ps1

# Deploy a production
.\scripts\deploy.ps1 -Production
```

### Verificaciones Pre-Deploy
- [ ] Todos los tests pasan
- [ ] Build exitoso
- [ ] Code review aprobado
- [ ] Documentación actualizada

## 🔧 Herramientas de Desarrollo

### VS Code Setup
El proyecto incluye configuraciones optimizadas:
- **Settings**: Formateo automático, autoguardado
- **Extensions**: Herramientas esenciales pre-configuradas
- **Tasks**: Comandos frecuentes automatizados
- **Snippets**: Plantillas de código

### Debugging
```json
// launch.json para debugging
{
  "type": "node",
  "request": "launch",
  "name": "Debug App",
  "program": "${workspaceFolder}/src/index.js",
  "env": {
    "NODE_ENV": "development"
  }
}
```

### Linting y Formatting
```bash
# Lint código
npm run lint

# Fix automático
npm run lint:fix

# Format código
npm run format
```

## 🌐 Trabajo Remoto

### Mejores Prácticas para Casa
- **Horarios consistentes**: Mantén rutina similar a la oficina
- **Espacio dedicado**: Área específica para trabajo
- **Breaks regulares**: Usa técnica Pomodoro
- **Comunicación proactiva**: Actualiza estado frecuentemente

### Mejores Prácticas para Oficina
- **Sincronización matutina**: Pull de cambios al llegar
- **Aprovecha recursos**: Usa mejor conexión para tareas pesadas
- **Colaboración presencial**: Pair programming cuando sea posible
- **Backup antes de salir**: Commit y push al final del día

### Herramientas de Colaboración
- **Git**: Control de versiones distribuido
- **VS Code Live Share**: Colaboración en tiempo real
- **Issues**: Tracking de bugs y features
- **Wiki**: Documentación compartida

## 📊 Monitoreo y Métricas

### Métricas de Desarrollo
- **Build time**: Tiempo de construcción
- **Test coverage**: Cobertura de tests
- **Bundle size**: Tamaño del build final
- **Performance**: Métricas de rendimiento

### Logs y Debugging
```javascript
// Logging estructurado
const logger = require('./utils/logger');

logger.info('User logged in', { userId: 123 });
logger.error('Database connection failed', { error: err.message });
```

### Análisis de Performance
```bash
# Profiling de la app
npm run profile

# Lighthouse audit
npm run audit:performance
```

## 🔐 Seguridad en Desarrollo

### Variables de Entorno
```bash
# .env (nunca commitear)
API_KEY=secret_key_here
DATABASE_URL=connection_string

# .env.example (sí commitear)
API_KEY=your_api_key_here
DATABASE_URL=your_database_url
```

### Validación de Input
```javascript
// Validar siempre inputs de usuario
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
```

### Secrets Management
- **Desarrollo**: Variables de entorno locales
- **Staging/Prod**: Servicios de secrets management
- **Nunca**: Hardcodear secrets en código

## 📚 Recursos Adicionales

### Documentación
- [Setup Guide](setup-guide.md) - Configuración inicial
- [API Documentation] - Documentación de API
- [Deployment Guide] - Guía de despliegue

### Enlaces Útiles
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Clean Code JavaScript](https://github.com/ryanmcdermott/clean-code-javascript)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

### Comunidad
- Slack: #infomilo-dev
- Email: dev-team@infomilo.com
- Issues: [GitHub Issues](link-to-issues)

# MiloBase - Templates Base del Sistema

Esta carpeta contiene todos los templates base y layouts principales que sirven como fundación para el resto de templates del sistema MiloApps.

## Estructura de Archivos

### Templates Base Principales

- `base.html` - Template base principal del sistema
- `layout.html` - Layout principal de la aplicación

## Uso en el Sistema

Todos los templates del sistema extienden de estos archivos base usando la nueva estructura:

```html
{% extends "MiloBase/base.html" %} {% extends "MiloBase/base_adapted.html" %} {%
extends "MiloBase/layout.html" %}
```

## Jerarquía de Templates

```
MiloBase/
├── base.html              # Base principal
└── layout.html           # Layout principal

└── Usados por:
    ├── index.html         # Página principal
    ├── error.html         # Páginas de error
    ├── docs.html         # Documentación
    ├── MiloAuth/         # Templates de autenticación
    └── MiloAdmin/        # Templates administrativos
```

## Características de los Templates Base

- ✅ **Responsive Design**: Bootstrap 5 integrado
- ✅ **FontAwesome Icons**: Iconos profesionales
- ✅ **Navigation**: Barra de navegación consistente
- ✅ **Flash Messages**: Sistema de mensajes integrado
- ✅ **SEO Friendly**: Meta tags y estructura optimizada
- ✅ **Cross-Browser**: Compatible con navegadores modernos

## Componentes Incluidos

### CSS y JavaScript

- Bootstrap 5.3+
- FontAwesome 6+
- Custom CSS para MiloApps
- JavaScript para interactividad

### Secciones Comunes

- Header con navegación
- Footer informativo
- Sistema de mensajes flash
- Blocks personalizables para contenido

## Modificaciones

Para hacer cambios que afecten a todo el sistema:

1. Editar el template base correspondiente en `MiloBase/`
2. Los cambios se propagarán automáticamente a todos los templates que lo extienden
3. Probar en diferentes módulos (Auth, Admin, etc.)

## Templates Especiales

- `layout.html` - Layout alternativo para casos específicos

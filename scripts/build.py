#!/usr/bin/env python3
# Build script para InfoMilo Flask App

import os
import shutil
import json
from datetime import datetime

print('🔨 Iniciando build de InfoMilo Flask App...')

# Crear directorio dist si no existe
dist_dir = os.path.join(os.path.dirname(__file__), '..', 'dist')
if not os.path.exists(dist_dir):
    os.makedirs(dist_dir, exist_ok=True)
    print('📁 Directorio dist creado')

# Copiar archivos fuente
src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
if os.path.exists(src_dir):
    # Copiar app.py y templates
    shutil.copy2(os.path.join(src_dir, 'app.py'), dist_dir)
    
    templates_src = os.path.join(src_dir, 'templates')
    templates_dist = os.path.join(dist_dir, 'templates')
    if os.path.exists(templates_src):
        if os.path.exists(templates_dist):
            shutil.rmtree(templates_dist)
        shutil.copytree(templates_src, templates_dist)
    
    print('📦 Archivos copiados a dist/')

# Copiar configuraciones
config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
config_dist = os.path.join(dist_dir, 'config')
if os.path.exists(config_dir):
    if os.path.exists(config_dist):
        shutil.rmtree(config_dist)
    shutil.copytree(config_dir, config_dist)
    print('⚙️  Configuraciones copiadas')

# Copiar requirements.txt
req_file = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
if os.path.exists(req_file):
    shutil.copy2(req_file, dist_dir)
    print('📋 requirements.txt copiado')

# Crear archivo de información del build
build_info = {
    'build_time': datetime.now().isoformat(),
    'version': '1.0.0',
    'environment': 'production',
    'files': []
}

for root, dirs, files in os.walk(dist_dir):
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), dist_dir)
        build_info['files'].append(rel_path)

with open(os.path.join(dist_dir, 'build-info.json'), 'w', encoding='utf-8') as f:
    json.dump(build_info, f, indent=2, ensure_ascii=False)

print('✅ Build completado exitosamente!')
print(f'📁 Archivos generados en: {dist_dir}')
print(f'📊 Total de archivos: {len(build_info["files"])}')
print('')
print('Para ejecutar en producción:')
print(f'  cd {dist_dir}')
print('  pip install -r requirements.txt')
print('  python app.py')

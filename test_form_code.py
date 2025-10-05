#!/usr/bin/env python
"""
Test directo del ProfileForm sin contexto Flask
"""
import sys
import os
sys.path.append('src')

# Inspeccionar el código del formulario directamente
def test_form_code():
    print("🧪 Inspeccionando código de ProfileForm...")
    
    try:
        # Leer el archivo forms.py y buscar la definición de ProfileForm
        with open('src/forms.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar la clase ProfileForm
        lines = content.split('\n')
        in_profile_form = False
        profile_form_lines = []
        
        for i, line in enumerate(lines):
            if 'class ProfileForm' in line:
                in_profile_form = True
                print(f"✅ Encontrado ProfileForm en línea {i+1}")
                
            if in_profile_form:
                profile_form_lines.append((i+1, line))
                
                # Parar cuando encontremos otra clase o final del archivo
                if line.strip().startswith('class ') and 'ProfileForm' not in line:
                    break
                    
        # Buscar campo bio
        bio_found = False
        for line_num, line in profile_form_lines:
            if 'bio' in line and '=' in line:
                print(f"✅ Campo 'bio' encontrado en línea {line_num}: {line.strip()}")
                bio_found = True
                
        if not bio_found:
            print("❌ Campo 'bio' NO encontrado en ProfileForm")
            
        # Mostrar estructura de la clase
        print("\n📋 Estructura de ProfileForm:")
        for line_num, line in profile_form_lines[:20]:  # Primeras 20 líneas
            if line.strip() and ('=' in line or 'def' in line or 'class' in line):
                print(f"   {line_num:3d}: {line.strip()}")
                
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")

if __name__ == '__main__':
    test_form_code()

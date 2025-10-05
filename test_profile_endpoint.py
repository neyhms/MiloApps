#!/usr/bin/env python
"""
Test específico para ProfileForm con contexto de Flask real
"""
import sys
import os
import requests
sys.path.append('src')

def test_profile_endpoint():
    """Probar acceso al endpoint de perfil"""
    print("🧪 Probando endpoint de perfil...")
    
    try:
        # Hacer login primero
        login_data = {
            'email': 'admin@infomilo.com',
            'password': 'admin123'
        }
        
        session = requests.Session()
        
        # Obtener página de login primero para CSRF token
        login_page = session.get('http://localhost:3000/auth/login')
        print(f"✅ Login page status: {login_page.status_code}")
        
        # Extraer CSRF token (simplificado)
        csrf_token = None
        if 'csrf_token' in login_page.text:
            import re
            match = re.search(r'csrf_token.*?value="([^"]+)"', login_page.text)
            if match:
                csrf_token = match.group(1)
                print(f"✅ CSRF token obtenido: {csrf_token[:20]}...")
        
        # Hacer login
        login_data['csrf_token'] = csrf_token
        login_response = session.post('http://localhost:3000/auth/login', data=login_data)
        print(f"✅ Login response status: {login_response.status_code}")
        
        # Acceder al perfil
        profile_response = session.get('http://localhost:3000/auth/profile')
        print(f"✅ Profile response status: {profile_response.status_code}")
        
        if profile_response.status_code == 500:
            print("❌ Error 500 en el perfil")
            if 'bio' in profile_response.text:
                print("🔍 El error menciona 'bio'")
        elif profile_response.status_code == 200:
            print("✅ Perfil cargado correctamente")
            if 'bio' in profile_response.text:
                print("✅ Campo 'bio' presente en la respuesta")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")

if __name__ == '__main__':
    test_profile_endpoint()

#!/usr/bin/env python
"""
Test del endpoint de registro
"""
import sys
import os
import requests
sys.path.append('src')

def test_registration():
    """Probar el registro de usuario"""
    print("🧪 Probando registro de usuario...")
    
    try:
        session = requests.Session()
        
        # Obtener página de registro primero para CSRF token
        register_page = session.get('http://localhost:3000/auth/register')
        print(f"✅ Register page status: {register_page.status_code}")
        
        # Extraer CSRF token
        csrf_token = None
        if 'csrf_token' in register_page.text:
            import re
            match = re.search(r'csrf_token.*?value="([^"]+)"', register_page.text)
            if match:
                csrf_token = match.group(1)
                print(f"✅ CSRF token obtenido: {csrf_token[:20]}...")
        
        # Datos de registro
        register_data = {
            'csrf_token': csrf_token,
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123',
            'password2': 'TestPassword123',
            'accept_terms': 'y',
            'phone': '',
            'company': '',
            'department': ''
        }
        
        # Hacer registro
        register_response = session.post('http://localhost:3000/auth/register', data=register_data)
        print(f"✅ Register response status: {register_response.status_code}")
        print(f"✅ Register response URL: {register_response.url}")
        
        # Verificar si hay errores en la respuesta
        if 'error' in register_response.text.lower() or 'invalid' in register_response.text.lower():
            print("⚠️  Posibles errores en la respuesta")
            
        # Verificar si nos redirigió al login
        if 'login' in register_response.url:
            print("✅ Redirigido al login - Registro exitoso")
        elif register_response.url.endswith('/register'):
            print("❌ Permaneció en registro - Posible error")
        
        # Verificar contenido
        if 'Registro exitoso' in register_response.text:
            print("✅ Mensaje de éxito encontrado")
        elif 'Error' in register_response.text:
            print("❌ Mensaje de error encontrado")
            
    except Exception as e:
        print(f"❌ Error en test: {e}")

if __name__ == '__main__':
    test_registration()

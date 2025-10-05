#!/usr/bin/env python3
"""
Script de prueba rápida para InfoMilo
Verifica que todos los endpoints principales respondan correctamente
"""

import requests
import sys

def test_endpoint(url, expected_status=200, description=""):
    """Probar un endpoint específico"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == expected_status:
            print(f"✅ {description}: {url} - Status {response.status_code}")
            return True
        else:
            print(f"❌ {description}: {url} - Status {response.status_code} (esperado {expected_status})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}: {url} - Error: {e}")
        return False

def main():
    """Ejecutar pruebas de endpoints"""
    base_url = "http://localhost:3000"
    
    print("🧪 Probando endpoints de InfoMilo...")
    print("=" * 50)
    
    tests = [
        (f"{base_url}/", "Página principal"),
        (f"{base_url}/auth/login", "Página de login"),
        (f"{base_url}/auth/register", "Página de registro"),
        (f"{base_url}/docs", "Documentación"),
        (f"{base_url}/api/status", "API Status"),
    ]
    
    passed = 0
    total = len(tests)
    
    for url, description in tests:
        if test_endpoint(url, description=description):
            passed += 1
    
    print("=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los endpoints funcionan correctamente!")
        return 0
    else:
        print("⚠️  Algunos endpoints tienen problemas")
        return 1

if __name__ == "__main__":
    sys.exit(main())

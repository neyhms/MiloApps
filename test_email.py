#!/usr/bin/env python
"""
Test de envío de email con Gmail SMTP
"""
import sys
import os
sys.path.append('src')

def test_email_service():
    """Probar el servicio de email"""
    print("🧪 Probando servicio de email...")
    
    # Crear contexto de aplicación Flask
    from app import InfoMiloApp
    app_instance = InfoMiloApp()
    app = app_instance.app
    
    with app.app_context():
        from email_service import send_email
        
        try:
            # Enviar email de prueba
            result = send_email(
                to='neyhms@gmail.com',  # Enviar a ti mismo para probar
                subject='Test de InfoMilo - Configuración SMTP',
                template='email_test',  # Crearemos una plantilla simple
                name='Usuario Test',
                message='Este es un email de prueba para verificar que el SMTP funciona correctamente.'
            )
            
            if result:
                print("✅ Email enviado exitosamente")
            else:
                print("❌ Error al enviar email")
                
        except Exception as e:
            print(f"❌ Error en envío de email: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_email_service()

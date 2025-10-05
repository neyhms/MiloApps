#!/usr/bin/env python
"""
Test script para verificar ProfileForm
"""
import sys
import os
sys.path.append('src')

def test_profile_form():
    print("🧪 Probando ProfileForm...")
    
    # Crear contexto de aplicación Flask
    from app import InfoMiloApp
    app_instance = InfoMiloApp()
    app = app_instance.app
    
    with app.app_context():
        from forms import ProfileForm
        
        try:
            # Crear instancia del formulario
            form = ProfileForm()
            
            # Verificar que tiene el atributo bio
            if hasattr(form, 'bio'):
                print("✅ El formulario tiene el campo 'bio'")
                print(f"   Tipo: {type(form.bio)}")
                print(f"   Etiqueta: {form.bio.label}")
            else:
                print("❌ El formulario NO tiene el campo 'bio'")
                
            # Listar todos los campos
            print("\n📋 Campos disponibles en ProfileForm:")
            for field_name, field in form._fields.items():
                print(f"   - {field_name}: {type(field).__name__}")
                
        except Exception as e:
            print(f"❌ Error al crear ProfileForm: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_profile_form()

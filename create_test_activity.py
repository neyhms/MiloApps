#!/usr/bin/env python3
"""Script para generar algunos registros de actividad de prueba"""

import os
import sys
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import db, AuditLog, User, AuditEvents
from app import MiloAppsApp

def create_test_activities():
    app = MiloAppsApp()
    
    with app.app.app_context():
        print("=== Creando registros de actividad de prueba ===")
        
        # Buscar usuario admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("❌ Usuario 'admin' no encontrado")
            return
            
        print(f"✅ Usuario encontrado: {admin.username}")
        
        # Crear algunos logs de actividad de prueba
        test_activities = [
            {
                'event_type': 'login_success',
                'event_description': 'Login exitoso desde navegador',
                'ip_address': '127.0.0.1',
                'browser': 'Chrome 119.0',
                'created_at': datetime.utcnow() - timedelta(minutes=5)
            },
            {
                'event_type': 'profile_update',
                'event_description': 'Perfil actualizado',
                'ip_address': '127.0.0.1',
                'browser': 'Chrome 119.0',
                'created_at': datetime.utcnow() - timedelta(minutes=15)
            },
            {
                'event_type': 'system_access',
                'event_description': 'Acceso al panel de administración',
                'ip_address': '127.0.0.1',
                'browser': 'Chrome 119.0',
                'created_at': datetime.utcnow() - timedelta(hours=1)
            },
            {
                'event_type': 'password_change',
                'event_description': 'Contraseña actualizada',
                'ip_address': '127.0.0.1',
                'browser': 'Chrome 119.0',
                'created_at': datetime.utcnow() - timedelta(hours=2)
            },
            {
                'event_type': 'data_access',
                'event_description': 'Consulta de datos del sistema',
                'ip_address': '127.0.0.1',
                'browser': 'Chrome 119.0',
                'created_at': datetime.utcnow() - timedelta(days=1)
            }
        ]
        
        for activity_data in test_activities:
            log = AuditLog(
                user_id=admin.id,
                event_type=activity_data['event_type'],
                event_description=activity_data['event_description'],
                ip_address=activity_data['ip_address'],
                browser=activity_data['browser'],
                success=True,
                created_at=activity_data['created_at']
            )
            db.session.add(log)
            print(f"➕ Agregado: {activity_data['event_description']}")
        
        db.session.commit()
        
        # Verificar que se crearon
        total_logs = AuditLog.query.filter_by(user_id=admin.id).count()
        print(f"✅ Total logs después de crear pruebas: {total_logs}")
        
        # Mostrar los últimos 5
        recent = AuditLog.query.filter_by(user_id=admin.id).order_by(AuditLog.created_at.desc()).limit(5).all()
        print("\n📋 Últimos 5 registros:")
        for i, log in enumerate(recent, 1):
            print(f"  {i}. {log.event_description} - {log.created_at}")

if __name__ == "__main__":
    create_test_activities()
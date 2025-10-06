#!/usr/bin/env python3
"""Script para debuggear la actividad del usuario"""

import os
import sys
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import db, AuditLog, User
from app import MiloAppsApp

def debug_user_activity():
    app = MiloAppsApp()
    
    with app.app.app_context():
        print("=== DEBUG: Actividad del Usuario ===")
        
        # Buscar usuario admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("❌ Usuario 'admin' no encontrado")
            return
            
        print(f"✅ Usuario encontrado: {admin.username}")
        print(f"📧 Email: {admin.email}")
        print(f"📅 Creado: {admin.created_at}")
        print(f"🔑 Último login: {admin.last_login}")
        print(f"⚡ Last activity field: {admin.last_activity}")
        
        # Contar logs de auditoría
        total_logs = AuditLog.query.filter_by(user_id=admin.id).count()
        print(f"📊 Total logs de auditoría: {total_logs}")
        
        # Mostrar últimos 5 logs
        recent_logs = AuditLog.query.filter_by(user_id=admin.id).order_by(AuditLog.created_at.desc()).limit(5).all()
        print(f"📋 Últimos {len(recent_logs)} logs:")
        
        for i, log in enumerate(recent_logs, 1):
            print(f"  {i}. {log.event_type} - {log.event_description}")
            print(f"     🕒 {log.created_at}")
            print(f"     🌐 {log.ip_address} | {log.browser}")
            
        # Probar el método get_last_activity
        print(f"\n🎯 Método get_last_activity(): {admin.get_last_activity()}")
        
        # Comparar con last_login
        if admin.last_login:
            diff = (admin.get_last_activity() - admin.last_login).total_seconds()
            print(f"🔄 Diferencia con last_login: {diff} segundos")

if __name__ == "__main__":
    debug_user_activity()
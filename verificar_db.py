#!/usr/bin/env python3
"""
Script para verificar registros en la base de datos de MiloApps
"""

import sqlite3
import os
from datetime import datetime

# Ruta a la base de datos
db_path = os.path.join(os.path.dirname(__file__), "data", "miloapps.db")


def verificar_base_datos():
    """Verificar el contenido de la base de datos"""
    print("🔍 Verificando base de datos MiloApps...")
    print(f"📍 Ruta: {db_path}")
    print("-" * 60)

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Listar todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()

        print("📋 Tablas en la base de datos:")
        for tabla in tablas:
            print(f"   • {tabla[0]}")

        print("-" * 60)

        # Verificar usuarios
        print("👥 USUARIOS:")
        cursor.execute(
            "SELECT id, username, email, created_at FROM users ORDER BY created_at DESC LIMIT 5;"
        )
        usuarios = cursor.fetchall()

        if usuarios:
            for user in usuarios:
                print(
                    f"   ID: {user[0]} | Usuario: {user[1]} | Email: {user[2]} | Creado: {user[3]}"
                )
        else:
            print("   ⚠️  No hay usuarios registrados")

        print("-" * 60)

        # Buscar tablas relacionadas con MiloTalent/Prestadores
        print("🔎 Buscando tablas de MiloTalent/Prestadores...")

        # Buscar por posibles nombres de tabla
        posibles_tablas = [
            "prestador",
            "prestadores",
            "milotalent",
            "talent",
            "service_provider",
        ]

        tablas_encontradas = []
        for tabla_nombre in posibles_tablas:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?;",
                (f"%{tabla_nombre}%",),
            )
            resultado = cursor.fetchall()
            if resultado:
                tablas_encontradas.extend([t[0] for t in resultado])

        if tablas_encontradas:
            print("✅ Tablas de MiloTalent encontradas:")
            for tabla in tablas_encontradas:
                print(f"   • {tabla}")

                # Mostrar contenido de cada tabla
                cursor.execute(f"SELECT * FROM {tabla} ORDER BY rowid DESC LIMIT 5;")
                registros = cursor.fetchall()

                if registros:
                    # Obtener nombres de columnas
                    cursor.execute(f"PRAGMA table_info({tabla});")
                    columnas = [col[1] for col in cursor.fetchall()]

                    print(f"   📊 Registros en {tabla}:")
                    for registro in registros:
                        print(
                            "   "
                            + " | ".join(
                                [
                                    f"{col}: {val}"
                                    for col, val in zip(columnas, registro)
                                ]
                            )
                        )
                else:
                    print(f"   ⚠️  No hay registros en {tabla}")
        else:
            print("⚠️  No se encontraron tablas específicas de MiloTalent")
            print("   Nota: Los datos podrían estar en otras tablas o el sistema")
            print("   podría estar usando un enfoque diferente para almacenar datos.")

        print("-" * 60)

        # Verificar logs de auditoría si existen
        print("📝 LOGS DE AUDITORÍA:")
        try:
            cursor.execute(
                "SELECT action, details, created_at FROM audit_log ORDER BY created_at DESC LIMIT 10;"
            )
            logs = cursor.fetchall()

            if logs:
                for log in logs:
                    print(f"   {log[2]} | {log[0]} | {log[1]}")
            else:
                print("   ⚠️  No hay logs de auditoría")
        except sqlite3.OperationalError:
            print("   ⚠️  Tabla audit_log no existe")

        conn.close()
        print("\n✅ Verificación completada")

    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")


if __name__ == "__main__":
    verificar_base_datos()

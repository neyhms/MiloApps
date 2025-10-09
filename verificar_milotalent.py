#!/usr/bin/env python3
"""
Script simplificado para verificar registros de MiloTalent
"""

import sqlite3
import os

# Ruta a la base de datos
db_path = os.path.join(os.path.dirname(__file__), "data", "miloapps.db")


def verificar_milotalent():
    """Verificar específicamente los datos de MiloTalent"""
    print("🔍 Verificando registros de MiloTalent...")
    print(f"📍 Base de datos: {db_path}")
    print("=" * 60)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Tablas de MiloTalent que encontramos
        tablas_talent = [
            "talent_prestadores",
            "talent_cdp",
            "talent_expedientes",
            "talent_historial_contratos",
            "talent_documentos",
            "talent_alertas",
            "talent_auditoria",
        ]

        for tabla in tablas_talent:
            print(f"\n📋 TABLA: {tabla.upper()}")
            print("-" * 40)

            try:
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
                total = cursor.fetchone()[0]
                print(f"📊 Total de registros: {total}")

                if total > 0:
                    # Mostrar estructura de la tabla
                    cursor.execute(f"PRAGMA table_info({tabla});")
                    columnas = cursor.fetchall()
                    print("🏗️  Estructura:")
                    for col in columnas:
                        print(f"   • {col[1]} ({col[2]})")

                    # Mostrar últimos registros
                    cursor.execute(
                        f"SELECT * FROM {tabla} ORDER BY rowid DESC LIMIT 3;"
                    )
                    registros = cursor.fetchall()

                    print("📄 Últimos registros:")
                    for i, registro in enumerate(registros, 1):
                        print(f"   Registro {i}:")
                        for j, valor in enumerate(registro):
                            col_nombre = (
                                columnas[j][1] if j < len(columnas) else f"col_{j}"
                            )
                            print(f"      {col_nombre}: {valor}")
                else:
                    print("   ⚠️  Sin registros")

            except sqlite3.Error as e:
                print(f"   ❌ Error: {e}")

        # Verificar usuarios también
        print(f"\n📋 TABLA: USERS")
        print("-" * 40)
        try:
            cursor.execute("SELECT COUNT(*) FROM users;")
            total_users = cursor.fetchone()[0]
            print(f"📊 Total de usuarios: {total_users}")

            if total_users > 0:
                cursor.execute(
                    "SELECT id, username, email FROM users ORDER BY id DESC LIMIT 3;"
                )
                usuarios = cursor.fetchall()
                print("👥 Últimos usuarios:")
                for user in usuarios:
                    print(f"   ID: {user[0]} | Usuario: {user[1]} | Email: {user[2]}")
        except sqlite3.Error as e:
            print(f"   ❌ Error: {e}")

        conn.close()
        print("\n✅ Verificación completada")

    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    verificar_milotalent()

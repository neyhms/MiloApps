#!/usr/bin/env python3
"""
Script para verificar los nuevos registros de MiloTalent
"""

import sqlite3
import os
import json

# Ruta a la base de datos
db_path = os.path.join(os.path.dirname(__file__), "data", "miloapps.db")


def verificar_nuevos_registros():
    """Verificar si hay nuevos registros después de la implementación"""
    print("🔍 Verificando nuevos registros en MiloTalent...")
    print("=" * 60)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar prestadores
        print("👥 PRESTADORES DE SERVICIO:")
        print("-" * 40)
        cursor.execute(
            """
            SELECT id_ps, cedula, nombre_completo, correo, telefono, 
                   perfil_profesional, sector_experiencia, modalidad, estado
            FROM talent_prestadores 
            ORDER BY id_ps DESC 
            LIMIT 5
        """
        )
        prestadores = cursor.fetchall()

        if prestadores:
            print(f"📊 Total encontrados: {len(prestadores)}")
            for i, p in enumerate(prestadores, 1):
                print(f"\n🆔 Prestador #{i}:")
                print(f"   ID: {p[0]}")
                print(f"   Cédula: {p[1]}")
                print(f"   Nombre: {p[2]}")
                print(f"   Email: {p[3]}")
                print(f"   Teléfono: {p[4]}")
                print(f"   Servicios: {p[5]}")
                print(f"   Sector: {p[6]}")
                print(f"   Modalidad: {p[7]}")
                print(f"   Estado: {p[8]}")
        else:
            print("   ⚠️  No hay prestadores registrados")

        # Verificar auditoría
        print(f"\n📝 REGISTROS DE AUDITORÍA:")
        print("-" * 40)
        cursor.execute(
            """
            SELECT id_auditoria, ps_id, usuario_id, accion, modulo, 
                   descripcion, fecha_accion, ip_usuario
            FROM talent_auditoria 
            ORDER BY fecha_accion DESC 
            LIMIT 5
        """
        )
        auditorias = cursor.fetchall()

        if auditorias:
            print(f"📊 Total de auditorías: {len(auditorias)}")
            for i, a in enumerate(auditorias, 1):
                print(f"\n📋 Auditoría #{i}:")
                print(f"   ID: {a[0]}")
                print(f"   PS ID: {a[1]}")
                print(f"   Usuario: {a[2]}")
                print(f"   Acción: {a[3]}")
                print(f"   Módulo: {a[4]}")
                print(f"   Descripción: {a[5]}")
                print(f"   Fecha: {a[6]}")
                print(f"   IP: {a[7]}")
        else:
            print("   ⚠️  No hay registros de auditoría")

        # Estadísticas generales
        print(f"\n📈 ESTADÍSTICAS:")
        print("-" * 40)

        # Contar por estado
        cursor.execute(
            "SELECT estado, COUNT(*) FROM talent_prestadores GROUP BY estado"
        )
        estados = cursor.fetchall()
        if estados:
            print("Por estado:")
            for estado, count in estados:
                print(f"   • {estado}: {count}")

        # Contar por modalidad
        cursor.execute(
            "SELECT modalidad, COUNT(*) FROM talent_prestadores GROUP BY modalidad"
        )
        modalidades = cursor.fetchall()
        if modalidades:
            print("Por modalidad:")
            for modalidad, count in modalidades:
                print(f"   • {modalidad}: {count}")

        conn.close()
        print(f"\n✅ Verificación completada")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    verificar_nuevos_registros()

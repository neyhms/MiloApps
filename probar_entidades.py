#!/usr/bin/env python3
"""
Prueba simple de las APIs de entidades usando SQL directo
"""

import sqlite3
import json

def probar_entidades():
    """Prueba las entidades directamente desde la base de datos"""
    
    print("🔍 PRUEBA DIRECTA DE ENTIDADES")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('data/miloapps.db')
        cursor = conn.cursor()
        
        # Verificar que la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='talent_entidades'")
        if not cursor.fetchone():
            print("❌ Tabla talent_entidades no existe")
            return
        
        print("✅ Tabla talent_entidades existe")
        
        # Obtener estadísticas por tipo
        cursor.execute("""
            SELECT tipo_entidad, COUNT(*) as total, 
                   SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activos
            FROM talent_entidades 
            GROUP BY tipo_entidad 
            ORDER BY tipo_entidad
        """)
        
        resultados = cursor.fetchall()
        
        print("\n📊 ENTIDADES EN BASE DE DATOS:")
        print("-" * 40)
        
        for tipo, total, activos in resultados:
            print(f"   {tipo.ljust(20)}: {activos}/{total} activos")
        
        # Probar algunas consultas específicas
        tipos_test = ['municipio', 'profesion', 'banco', 'eps']
        
        print("\n🔍 MUESTRA DE DATOS:")
        print("-" * 40)
        
        for tipo in tipos_test:
            cursor.execute("""
                SELECT nombre FROM talent_entidades 
                WHERE tipo_entidad = ? AND activo = 1 
                ORDER BY orden, nombre 
                LIMIT 3
            """, (tipo,))
            
            entidades = cursor.fetchall()
            nombres = [ent[0] for ent in entidades]
            
            if nombres:
                print(f"   {tipo}: {', '.join(nombres)}...")
            else:
                print(f"   {tipo}: Sin datos")
        
        # Crear datos de prueba para la API
        print("\n🌐 SIMULACIÓN DE API:")
        print("-" * 40)
        
        for tipo in ['municipio', 'profesion', 'banco']:
            cursor.execute("""
                SELECT id, codigo, nombre, descripcion, departamento, activo
                FROM talent_entidades 
                WHERE tipo_entidad = ? AND activo = 1 
                ORDER BY orden, nombre 
                LIMIT 5
            """, (tipo,))
            
            entidades = cursor.fetchall()
            
            api_data = []
            for ent in entidades:
                api_data.append({
                    'id': ent[0],
                    'codigo': ent[1],
                    'nombre': ent[2],
                    'descripcion': ent[3],
                    'departamento': ent[4],
                    'activo': bool(ent[5])
                })
            
            print(f"   /api/{tipo}: {len(api_data)} registros disponibles")
            if api_data:
                print(f"      Ejemplo: {api_data[0]['nombre']}")
        
        conn.close()
        print("\n🎉 BASE DE DATOS FUNCIONANDO CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    probar_entidades()
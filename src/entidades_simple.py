"""
Rutas simplificadas para entidades - versión de emergencia
"""

from flask import Blueprint, jsonify
import sqlite3
import os

# Blueprint simple para entidades
entidades_simple_bp = Blueprint('entidades_simple', __name__, url_prefix='/admin/entidades')

def get_db_connection():
    """Obtener conexión a la base de datos"""
    db_path = os.path.join('data', 'miloapps.db')
    return sqlite3.connect(db_path)

@entidades_simple_bp.route('/api/<tipo>')
def api_entidades_simple(tipo):
    """API simplificada para obtener entidades por tipo"""
    
    tipos_validos = [
        'municipio', 'profesion', 'banco', 'eps', 'afp', 'arl', 
        'caja_compensacion', 'operador_ss', 'area_personal'
    ]
    
    if tipo not in tipos_validos:
        return jsonify({'error': 'Tipo de entidad no válido'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, codigo, nombre, descripcion, departamento, codigo_dane,
                   nit, telefono, email, direccion, es_obligatorio, permite_otros, 
                   orden, activo
            FROM talent_entidades 
            WHERE tipo_entidad = ? AND activo = 1 
            ORDER BY orden, nombre
        """, (tipo,))
        
        resultados = cursor.fetchall()
        
        entidades = []
        for resultado in resultados:
            entidades.append({
                'id': resultado[0],
                'codigo': resultado[1],
                'nombre': resultado[2],
                'descripcion': resultado[3],
                'departamento': resultado[4],
                'codigo_dane': resultado[5],
                'nit': resultado[6],
                'telefono': resultado[7],
                'email': resultado[8],
                'direccion': resultado[9],
                'es_obligatorio': bool(resultado[10]),
                'permite_otros': bool(resultado[11]),
                'orden': resultado[12],
                'activo': bool(resultado[13])
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': entidades,
            'tipo': tipo,
            'total': len(entidades)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@entidades_simple_bp.route('/api/all')
def api_todas_entidades_simple():
    """API para obtener todas las entidades agrupadas por tipo"""
    
    tipos = [
        'municipio', 'profesion', 'banco', 'eps', 'afp', 'arl', 
        'caja_compensacion', 'operador_ss', 'area_personal'
    ]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        resultado = {}
        
        for tipo in tipos:
            cursor.execute("""
                SELECT id, codigo, nombre, descripcion, departamento, codigo_dane,
                       nit, telefono, email, direccion, es_obligatorio, permite_otros, 
                       orden, activo
                FROM talent_entidades 
                WHERE tipo_entidad = ? AND activo = 1 
                ORDER BY orden, nombre
            """, (tipo,))
            
            entidades = []
            for row in cursor.fetchall():
                entidades.append({
                    'id': row[0],
                    'codigo': row[1],
                    'nombre': row[2],
                    'descripcion': row[3],
                    'departamento': row[4],
                    'codigo_dane': row[5],
                    'nit': row[6],
                    'telefono': row[7],
                    'email': row[8],
                    'direccion': row[9],
                    'es_obligatorio': bool(row[10]),
                    'permite_otros': bool(row[11]),
                    'orden': row[12],
                    'activo': bool(row[13])
                })
            
            resultado[tipo] = entidades
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': resultado,
            'tipos': tipos
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@entidades_simple_bp.route('/test')
def test_entidades():
    """Endpoint de prueba para verificar que el blueprint funciona"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM talent_entidades WHERE activo = 1")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT tipo_entidad, COUNT(*) 
            FROM talent_entidades 
            WHERE activo = 1 
            GROUP BY tipo_entidad
        """)
        
        por_tipo = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Blueprint de entidades funcionando',
            'total_entidades': total,
            'por_tipo': por_tipo
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
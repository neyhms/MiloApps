#!/usr/bin/env python3
"""
Script de migración para convertir campos de texto de municipios 
a referencias de la tabla talent_municipios
"""

import sqlite3
from datetime import datetime
import os
import re

def migrar_municipios():
    """Migra los datos existentes a la nueva estructura."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 INICIANDO MIGRACIÓN DE MUNICIPIOS")
        print("=" * 50)
        
        # 1. Verificar estructura actual
        cursor.execute("PRAGMA table_info(talent_prestadores_new)")
        columns = [col[1] for col in cursor.fetchall()]
        
        tiene_campos_antiguos = any(col in columns for col in ['expedida', 'ciudad_nacimiento', 'municipio_residencia'])
        tiene_campos_nuevos = any(col in columns for col in ['expedida_id', 'ciudad_nacimiento_id', 'municipio_residencia_id'])
        
        print(f"📋 Campos antiguos presentes: {tiene_campos_antiguos}")
        print(f"📋 Campos nuevos presentes: {tiene_campos_nuevos}")
        
        if not tiene_campos_antiguos:
            print("✅ No hay campos antiguos para migrar")
            return True
        
        # 2. Obtener registros a migrar
        cursor.execute("""
            SELECT id, expedida, ciudad_nacimiento, municipio_residencia 
            FROM talent_prestadores_new 
            WHERE expedida IS NOT NULL OR ciudad_nacimiento IS NOT NULL OR municipio_residencia IS NOT NULL
        """)
        
        registros = cursor.fetchall()
        print(f"📊 Encontrados {len(registros)} registros para migrar")
        
        if not registros:
            print("✅ No hay registros para migrar")
            return True
        
        # 3. Obtener municipios disponibles
        cursor.execute("SELECT id, nombre, departamento, nombre_completo FROM talent_municipios WHERE activo = 1")
        municipios = cursor.fetchall()
        municipios_dict = {}
        
        for mun_id, nombre, departamento, nombre_completo in municipios:
            # Crear índices para búsqueda
            municipios_dict[nombre_completo.upper()] = mun_id
            municipios_dict[nombre.upper()] = mun_id
            municipios_dict[f"{nombre.upper()} - {departamento.upper()}"] = mun_id
            municipios_dict[f"{nombre.upper()} ({departamento.upper()})"] = mun_id
            municipios_dict[f"{nombre.upper()} {departamento.upper()}"] = mun_id
        
        print(f"📋 {len(municipios)} municipios disponibles para mapear")
        
        # 4. Migrar cada registro
        migrados = 0
        no_encontrados = []
        
        for ps_id, expedida, ciudad_nacimiento, municipio_residencia in registros:
            
            # Buscar municipio para expedida
            expedida_id = None
            if expedida:
                expedida_clean = limpiar_municipio(expedida)
                expedida_id = buscar_municipio_id(expedida_clean, municipios_dict)
                if not expedida_id:
                    no_encontrados.append(f"Expedida: {expedida}")
            
            # Buscar municipio para ciudad_nacimiento
            ciudad_nacimiento_id = None
            if ciudad_nacimiento:
                ciudad_clean = limpiar_municipio(ciudad_nacimiento)
                ciudad_nacimiento_id = buscar_municipio_id(ciudad_clean, municipios_dict)
                if not ciudad_nacimiento_id:
                    no_encontrados.append(f"Ciudad nacimiento: {ciudad_nacimiento}")
            
            # Buscar municipio para municipio_residencia
            municipio_residencia_id = None
            if municipio_residencia:
                residencia_clean = limpiar_municipio(municipio_residencia)
                municipio_residencia_id = buscar_municipio_id(residencia_clean, municipios_dict)
                if not municipio_residencia_id:
                    no_encontrados.append(f"Municipio residencia: {municipio_residencia}")
            
            # Actualizar registro si encontramos al menos un municipio
            if expedida_id or ciudad_nacimiento_id or municipio_residencia_id:
                updates = []
                params = []
                
                if expedida_id:
                    updates.append("expedida_id = ?")
                    params.append(expedida_id)
                
                if ciudad_nacimiento_id:
                    updates.append("ciudad_nacimiento_id = ?")
                    params.append(ciudad_nacimiento_id)
                
                if municipio_residencia_id:
                    updates.append("municipio_residencia_id = ?")
                    params.append(municipio_residencia_id)
                
                params.append(ps_id)
                
                cursor.execute(f"""
                    UPDATE talent_prestadores_new 
                    SET {', '.join(updates)}
                    WHERE id = ?
                """, params)
                
                migrados += 1
        
        conn.commit()
        
        print(f"\n✅ MIGRACIÓN COMPLETADA:")
        print(f"   - Registros migrados: {migrados}")
        print(f"   - Municipios no encontrados: {len(set(no_encontrados))}")
        
        if no_encontrados:
            print(f"\n⚠️  MUNICIPIOS NO ENCONTRADOS:")
            for municipio in sorted(set(no_encontrados)):
                print(f"   - {municipio}")
            print("\n💡 Sugerencia: Crear estos municipios en la administración")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error con la base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    finally:
        if conn:
            conn.close()

def limpiar_municipio(texto):
    """Limpia y normaliza el texto del municipio."""
    if not texto:
        return ""
    
    # Convertir a mayúsculas
    texto = texto.upper().strip()
    
    # Remover caracteres especiales comunes
    texto = re.sub(r'[().]', '', texto)
    
    # Normalizar espacios
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto

def buscar_municipio_id(texto_buscar, municipios_dict):
    """Busca el ID del municipio en el diccionario."""
    if not texto_buscar:
        return None
    
    # Búsqueda exacta
    if texto_buscar in municipios_dict:
        return municipios_dict[texto_buscar]
    
    # Búsqueda por similitud
    for key, mun_id in municipios_dict.items():
        if texto_buscar in key or key in texto_buscar:
            return mun_id
    
    # Búsqueda por partes (nombre del municipio)
    palabras = texto_buscar.split()
    for palabra in palabras:
        if len(palabra) > 3:  # Solo palabras significativas
            for key, mun_id in municipios_dict.items():
                if palabra in key:
                    return mun_id
    
    return None

if __name__ == "__main__":
    print("🔄 MIGRACIÓN DE MUNICIPIOS - CAMPOS TEXTO A REFERENCIAS")
    print("=" * 60)
    
    resultado = migrar_municipios()
    
    if resultado:
        print("\n🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("📝 Los registros ahora usan referencias a la tabla de municipios")
        print("🔗 Puedes verificar en: http://localhost:3000/milotalent/listado")
    else:
        print("\n❌ Error en la migración")
        print("   Revisa los mensajes de error anteriores")
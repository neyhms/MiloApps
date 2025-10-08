#!/usr/bin/env python3
"""
Script para poblar entidades usando SQL directo
"""

import sqlite3
import os
from datetime import datetime

def main():
    print("🚀 POBLANDO ENTIDADES TALENT")
    print("=" * 40)
    
    db_path = os.path.join('data', 'miloapps.db')
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Datos de entidades básicas
    entidades = [
        # Municipios principales
        ('municipio', '11001', 'Bogotá D.C.', '', 'Bogotá D.C.', '11001', '', '', '', '', 1, 0, 1, 1),
        ('municipio', '05001', 'Medellín', '', 'Antioquia', '05001', '', '', '', '', 1, 0, 2, 1),
        ('municipio', '76001', 'Cali', '', 'Valle del Cauca', '76001', '', '', '', '', 1, 0, 3, 1),
        ('municipio', '08001', 'Barranquilla', '', 'Atlántico', '08001', '', '', '', '', 1, 0, 4, 1),
        ('municipio', '13001', 'Cartagena', '', 'Bolívar', '13001', '', '', '', '', 1, 0, 5, 1),
        
        # Profesiones
        ('profesion', 'ING_SIS', 'Ingeniero de Sistemas', '', '', '', '', '', '', '', 1, 0, 1, 1),
        ('profesion', 'MED_GEN', 'Médico General', '', '', '', '', '', '', '', 1, 0, 2, 1),
        ('profesion', 'ABOGADO', 'Abogado', '', '', '', '', '', '', '', 1, 0, 3, 1),
        ('profesion', 'CONT_PUB', 'Contador Público', '', '', '', '', '', '', '', 1, 0, 4, 1),
        ('profesion', 'ADM_EMP', 'Administrador de Empresas', '', '', '', '', '', '', '', 1, 0, 5, 1),
        ('profesion', 'PSICOLOGO', 'Psicólogo', '', '', '', '', '', '', '', 1, 0, 6, 1),
        ('profesion', 'ENFERMERO', 'Enfermero', '', '', '', '', '', '', '', 1, 0, 7, 1),
        ('profesion', 'OTROS', 'Otros', '', '', '', '', '', '', '', 1, 1, 10, 1),
        
        # Bancos principales
        ('banco', '007', 'Bancolombia', '', '', '', '890903938-8', '', '', '', 1, 0, 1, 1),
        ('banco', '001', 'Banco de Bogotá', '', '', '', '860002964-4', '', '', '', 1, 0, 2, 1),
        ('banco', '002', 'Banco Popular', '', '', '', '860007738-9', '', '', '', 1, 0, 3, 1),
        ('banco', '013', 'BBVA Colombia', '', '', '', '860003020-1', '', '', '', 1, 0, 4, 1),
        ('banco', '051', 'Banco Davivienda', '', '', '', '860034313-7', '', '', '', 1, 0, 5, 1),
        ('banco', 'OTROS', 'Otros', '', '', '', '', '', '', '', 1, 1, 10, 1),
        
        # EPS principales
        ('eps', 'EPS001', 'Sura EPS', '', '', '', '800088702-2', '', '', '', 1, 0, 1, 1),
        ('eps', 'EPS002', 'Nueva EPS', '', '', '', '900156264-3', '', '', '', 1, 0, 2, 1),
        ('eps', 'EPS003', 'Sanitas EPS', '', '', '', '800251440-6', '', '', '', 1, 0, 3, 1),
        ('eps', 'EPS004', 'Salud Total EPS', '', '', '', '800130907-4', '', '', '', 1, 0, 4, 1),
        ('eps', 'EPS005', 'Compensar EPS', '', '', '', '860002503-1', '', '', '', 1, 0, 5, 1),
        ('eps', 'OTROS', 'Otros', '', '', '', '', '', '', '', 1, 1, 10, 1),
        
        # AFP principales
        ('afp', 'AFP001', 'Protección AFP', '', '', '', '800156998-0', '', '', '', 1, 0, 1, 1),
        ('afp', 'AFP002', 'Porvenir AFP', '', '', '', '800144331-3', '', '', '', 1, 0, 2, 1),
        ('afp', 'AFP003', 'Colfondos AFP', '', '', '', '800008578-7', '', '', '', 1, 0, 3, 1),
        ('afp', 'COLP001', 'Colpensiones', '', '', '', '900336259-7', '', '', '', 1, 0, 4, 1),
        ('afp', 'OTROS', 'Otros', '', '', '', '', '', '', '', 1, 1, 10, 1),
        
        # ARL principales
        ('arl', 'ARL001', 'Sura ARL', '', '', '', '800088702-2', '', '', '', 1, 0, 1, 1),
        ('arl', 'ARL002', 'Positiva ARL', '', '', '', '800053635-1', '', '', '', 1, 0, 2, 1),
        ('arl', 'ARL003', 'Colmena ARL', '', '', '', '860002180-3', '', '', '', 1, 0, 3, 1),
        ('arl', 'ARL004', 'Liberty ARL', '', '', '', '860002183-8', '', '', '', 1, 0, 4, 1),
        ('arl', 'OTROS', 'Otros', '', '', '', '', '', '', '', 1, 1, 10, 1),
        
        # Caja de Compensación (opcional)
        ('caja_compensacion', 'COMP001', 'Compensar', '', '', '', '860002503-1', '', '', '', 0, 0, 1, 1),
        ('caja_compensacion', 'CAFAM001', 'Cafam', '', '', '', '860007387-5', '', '', '', 0, 0, 2, 1),
        ('caja_compensacion', 'COLS001', 'Colsubsidio', '', '', '', '860007386-7', '', '', '', 0, 0, 3, 1),
        ('caja_compensacion', 'NA', 'No Aplica', '', '', '', '', '', '', '', 0, 0, 8, 1),
        ('caja_compensacion', 'OTROS', 'Otros', '', '', '', '', '', '', '', 0, 1, 10, 1),
        
        # Operador Seguridad Social
        ('operador_ss', 'AEL001', 'Aportes en Línea', '', '', '', '900156264-3', '', '', '', 1, 0, 1, 1),
        ('operador_ss', 'MIP001', 'Mi Planilla', '', '', '', '900337082-0', '', '', '', 1, 0, 2, 1),
        ('operador_ss', 'SIM001', 'Simple', '', '', '', '900930737-0', '', '', '', 1, 0, 3, 1),
        ('operador_ss', 'SOI001', 'SOI Planilla Integrada', '', '', '', '900156264-3', '', '', '', 1, 0, 4, 1),
        ('operador_ss', 'OTROS', 'Otros', '', '', '', '', '', '', '', 1, 1, 10, 1),
        
        # Área de Personal (pueden variar)
        ('area_personal', 'RH001', 'Recursos Humanos', '', '', '', '', '', '', '', 1, 0, 1, 1),
        ('area_personal', 'TH001', 'Talento Humano', '', '', '', '', '', '', '', 1, 0, 2, 1),
        ('area_personal', 'GH001', 'Gestión Humana', '', '', '', '', '', '', '', 1, 0, 3, 1),
        ('area_personal', 'AP001', 'Administración de Personal', '', '', '', '', '', '', '', 1, 0, 4, 1),
        ('area_personal', 'NOM001', 'Nómina', '', '', '', '', '', '', '', 1, 0, 5, 1),
        ('area_personal', 'OTROS', 'Otros', '', '', '', '', '', '', '', 1, 1, 10, 1),
    ]
    
    # Limpiar datos existentes
    cursor.execute("DELETE FROM talent_entidades")
    print("🧹 Datos existentes eliminados")
    
    # Insertar nuevos datos
    now = datetime.utcnow().isoformat()
    
    insertadas = 0
    for entidad in entidades:
        try:
            cursor.execute("""
                INSERT INTO talent_entidades (
                    tipo_entidad, codigo, nombre, descripcion, departamento, codigo_dane,
                    nit, telefono, email, direccion, es_obligatorio, permite_otros, orden, activo,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, entidad + (now, now))
            insertadas += 1
        except Exception as e:
            print(f"❌ Error insertando {entidad[2]}: {e}")
    
    conn.commit()
    print(f"✅ {insertadas} entidades insertadas")
    
    # Mostrar estadísticas
    tipos = ['municipio', 'profesion', 'banco', 'eps', 'afp', 'arl', 'caja_compensacion', 'operador_ss', 'area_personal']
    print("\n📊 ESTADÍSTICAS:")
    for tipo in tipos:
        cursor.execute("SELECT COUNT(*) FROM talent_entidades WHERE tipo_entidad = ? AND activo = 1", (tipo,))
        count = cursor.fetchone()[0]
        print(f"   {tipo}: {count} registros")
    
    cursor.execute("SELECT COUNT(*) FROM talent_entidades WHERE activo = 1")
    total = cursor.fetchone()[0]
    print(f"\n📈 TOTAL: {total} entidades activas")
    
    conn.close()
    print("\n🎉 POBLADO COMPLETADO")

if __name__ == "__main__":
    main()
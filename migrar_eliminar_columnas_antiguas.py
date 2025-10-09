import sqlite3

DB_PATH = 'data/miloapps.db'
TABLE = 'talent_prestadores_new'

# Columnas antiguas a eliminar
columnas_antiguas = [
    'profesion', 'banco', 'eps', 'afp', 'arl', 'caja', 'operador_ss', 'area_personal'
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Obtener columnas actuales
c.execute(f'PRAGMA table_info({TABLE})')
cols = c.fetchall()

# Generar lista de columnas a conservar
cols_nuevas = [col[1] for col in cols if col[1] not in columnas_antiguas]
cols_nuevas_str = ', '.join(cols_nuevas)

print('Columnas nuevas:', cols_nuevas_str)

# Crear tabla temporal sin columnas antiguas
c.execute(f"""
    CREATE TABLE {TABLE}_tmp AS SELECT {cols_nuevas_str} FROM {TABLE};
""")

# Eliminar tabla original
c.execute(f"DROP TABLE {TABLE};")

# Renombrar tabla temporal
c.execute(f"ALTER TABLE {TABLE}_tmp RENAME TO {TABLE};")

conn.commit()
conn.close()
print('Columnas antiguas eliminadas correctamente.')

# migrar_eliminar_profesion.py
"""
Script para eliminar la columna antigua 'profesion' de la tabla talent_prestadores_new.
"""
import sqlite3

DB_PATH = 'data/miloapps.db'
TABLE = 'talent_prestadores_new'
COLUMN = 'profesion'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Verificar si la columna existe
c.execute(f"PRAGMA table_info({TABLE})")
columns = [row[1] for row in c.fetchall()]
if COLUMN in columns:
    print(f"Eliminando columna '{COLUMN}' de la tabla '{TABLE}'...")
    # 2. Crear nueva tabla sin la columna 'profesion'
    c.execute(f"""
        CREATE TABLE {TABLE}_tmp AS SELECT * FROM {TABLE} WHERE 1=0;
    """)
    c.execute(f"PRAGMA table_info({TABLE})")
    col_defs = [f"{row[1]} {row[2]}" for row in c.fetchall() if row[1] != COLUMN]
    col_names = [row[1] for row in c.fetchall() if row[1] != COLUMN]
    c.execute(f"DROP TABLE IF EXISTS {TABLE}_tmp")
    c.execute(f"CREATE TABLE {TABLE}_tmp ({', '.join(col_defs)})")
    c.execute(f"INSERT INTO {TABLE}_tmp SELECT {', '.join(col_names)} FROM {TABLE}")
    c.execute(f"DROP TABLE {TABLE}")
    c.execute(f"ALTER TABLE {TABLE}_tmp RENAME TO {TABLE}")
    conn.commit()
    print(f"Columna '{COLUMN}' eliminada correctamente.")
else:
    print(f"La columna '{COLUMN}' no existe en la tabla '{TABLE}'. Nada que hacer.")

conn.close()
print("Migración completada.")

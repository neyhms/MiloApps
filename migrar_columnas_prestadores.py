import sqlite3

DB_PATH = 'data/miloapps.db'
TABLE = 'talent_prestadores_new'

# Columnas nuevas que deben existir según el modelo
COLUMNS = [
    'profesion_id INTEGER',
    'banco_id INTEGER',
    'eps_id INTEGER',
    'afp_id INTEGER',
    'arl_id INTEGER',
    'caja_compensacion_id INTEGER',
    'operador_ss_id INTEGER',
    'area_personal_id INTEGER'
]

# Verifica y agrega columnas si no existen
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

for col_def in COLUMNS:
    col_name = col_def.split()[0]
    c.execute(f"PRAGMA table_info({TABLE})")
    columns = [row[1] for row in c.fetchall()]
    if col_name not in columns:
        print(f"Agregando columna: {col_name}")
        c.execute(f"ALTER TABLE {TABLE} ADD COLUMN {col_def}")
    else:
        print(f"Columna ya existe: {col_name}")

conn.commit()
conn.close()
print("✅ Migración de columnas completada.")

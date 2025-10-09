import sqlite3

conn = sqlite3.connect('data/miloapps.db')
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("📊 TABLAS EXISTENTES:")
for table in tables:
    print(f"   - {table[0]}")

conn.close()
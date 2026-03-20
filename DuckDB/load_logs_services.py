import duckdb

# Conectar a DuckDB (en memoria - los datos se pierden al cerrar)
con = duckdb.connect()

# DuckDB puede leer JSON directamente
con.execute(
    """
    CREATE TABLE logs_services AS 
    SELECT * FROM read_json_auto('Logs de Servidor/Dataset/logs_services.json')
"""
)

# Verificar que cargó bien
print("Total de filas:", con.execute("SELECT COUNT(*) FROM logs_services").fetchone()[0])

# Ver estructura de la tabla (igual que en PostgreSQL)
print("\nColumnas:")
for col in con.execute("DESCRIBE logs_services").fetchall():
    print(f"  {col[0]}: {col[1]}")

# Ver primeras filas
print("\nPrimeras 3 filas:")
print(con.execute("SELECT * FROM logs_services LIMIT 3").fetchdf())
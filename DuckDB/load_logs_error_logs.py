import duckdb

# Conectar a DuckDB (en memoria - los datos se pierden al cerrar)
con = duckdb.connect()

# DuckDB puede leer JSON directamente
con.execute(
    """
    CREATE TABLE logs_error_logs AS 
    SELECT * FROM read_json_auto('Logs de Servidor/Dataset/logs_error_logs.json')
"""
)

# ========================================
print('\n2. ERRORES MÁS COMUNES')
# ========================================
print('¿Qué errores son los más críticos? ¿A cuántos usuarios afectan?\n')

print(con.execute(
    """
    SELECT 
        error_type,
        --error_message,
        COUNT(*) as total_errors
    FROM logs_error_logs
    GROUP BY 1--, 2
    ORDER BY 2 DESC
"""
).fetchdf())
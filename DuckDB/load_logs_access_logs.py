import duckdb

# Conectar a DuckDB (en memoria - los datos se pierden al cerrar)
con = duckdb.connect()

# DuckDB puede leer JSON directamente
con.execute(
    """
    CREATE TABLE logs_access_logs AS 
    SELECT * FROM read_json_auto('Logs de Servidor/Dataset/logs_access_logs.json')
"""
)

# Verificar que cargó bien
print("Total de filas:", con.execute("SELECT COUNT(*) FROM logs_access_logs").fetchone()[0])

# Ver estructura de la tabla (igual que en PostgreSQL)
print("\nColumnas:")
for col in con.execute("DESCRIBE logs_access_logs").fetchall():
    print(f"  {col[0]}: {col[1]}")

# Ver primeras filas
print("\nPrimeras 3 filas:")
print(con.execute("SELECT * FROM logs_access_logs LIMIT 3").fetchdf())

# ========================================
print('\n1. EXPLORACIÓN INICIAL')
# ========================================
print('¿Cuántos registros? ¿Qué período cubren?\n')

print(con.execute(
    """
    SELECT 
        COUNT(*) as total_requests,
        MIN(timestamp) as primera_request,
        MAX(timestamp) as ultima_request,
        COUNT(DISTINCT user_id) as usuarios_unicos,
        COUNT(DISTINCT endpoint) as endpoints_unicos
    FROM logs_access_logs
"""
).fetchdf())


# ========================================
print('\n2. ENDPOINTS MÁS USADOS')
# ========================================
print('¿Qué endpoints reciben más tráfico?\n')

print(con.execute(
    """
    SELECT 
        endpoint,
        COUNT(*) as total_requests,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM logs_access_logs), 2) as porcentaje
    FROM logs_access_logs
    GROUP BY 1
    ORDER BY 2 DESC
"""
).fetchdf())

# ========================================
print('\n3. ANÁLISIS DE ERRORES')
# ========================================
print('¿Qué endpoints tienen más errores 500?\n')

print(con.execute(
"""
    SELECT 
        endpoint,
        COUNT(*) as total_errors,
        COUNT(DISTINCT user_id) as usuarios_afectados,
        ROUND(AVG(response_time_ms), 2) as avg_response_time
    FROM logs_access_logs
    WHERE status_code >= 500
    GROUP BY endpoint
    ORDER BY total_errors DESC
    LIMIT 10
"""
).fetchdf())

# ========================================
print('\n4. PERFORMANCE POR ENDPOINT')
# ========================================
print('¿Qué endpoints son más lentos?\n')

print(con.execute(
"""
    SELECT 
        endpoint,
        COUNT(*) as requests,
        ROUND(AVG(response_time_ms), 2) as avg_time,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY response_time_ms), 2) as p50,
        ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms), 2) as p95,
        MAX(response_time_ms) as max_time
    FROM logs_access_logs
    WHERE status_code < 500
    GROUP BY endpoint
    --HAVING requests > 100
    ORDER BY 3 DESC
    LIMIT 10
"""
).fetchdf())

# ========================================
print('\n5. TENDENCIA HORARIA')
# ========================================
print('¿A qué hora hay más tráfico?\n')

print(con.execute(
"""
    SELECT 
        EXTRACT(HOUR FROM timestamp) as hora,
        COUNT(*) as requests,
        ROUND(AVG(response_time_ms), 2) as avg_time,
        SUM(CASE WHEN status_code >= 500 THEN 1 ELSE 0 END) as errors
    FROM logs_access_logs
    GROUP BY 1
    ORDER BY 1
"""
).fetchdf())

# ========================================
print('\n6. WINDOW FUNCTIONS - RANKING')
# ========================================
print('Top 3 requests más lentas por endpoint\n')

print(con.execute(
"""
    WITH ranked as (
        SELECT endpoint, 
            timestamp,
            response_time_ms,
            user_id,
            ROW_NUMBER() OVER (PARTITION BY endpoint ORDER BY response_time_ms DESC) as rn
        FROM logs_access_logs
        WHERE status_code < 500
    )
    SELECT *
    FROM ranked
    WHERE rn <= 3
    LIMIT 15
"""
).fetchdf())

# ========================================
print('\n7. COMPARACIÓN CON PERÍODO ANTERIOR')
# ========================================
print('¿Cómo cambia el tráfico día a día?\n')

print(con.execute(
"""
    WITH daily_stats AS (
    SELECT 
        timestamp::date AS fecha,
        COUNT(*) AS requests,
        ROUND(AVG(response_time_ms), 2) AS avg_time
    FROM logs_access_logs
    GROUP BY 1
    )
    SELECT fecha
        , requests
        , lag(requests) OVER (ORDER BY fecha) AS prev_requests
        , requests - prev_requests AS requests_diff
        , (requests / prev_requests - 1) * 100 as requests_diff_pct 
        , avg_time
        , lag(avg_time) OVER (ORDER BY fecha) AS prev_avg_time
        , avg_time - prev_avg_time AS avg_time_diff
        , (avg_time / prev_avg_time - 1) * 100 as avg_time_diff_pct
    FROM daily_stats
"""
).fetchdf())
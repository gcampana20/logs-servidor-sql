
# Análisis SQL de Logs de Servidor

## Descripción
Analizá logs de servidor web reales para encontrar patrones, errores y oportunidades de optimización.

## Herramientas
- VSC
- duckDB
- Archivos .json o .parquet

## Cómo correr

pip install duckdb

# Lo que hace este código:

→ duckdb.connect() - Crea una base de datos en memoria
→ read_json_auto() - Lee el JSON y detecta los tipos automáticamente
→ CREATE TABLE ... AS SELECT - Crea la tabla con los datos
→ DESCRIBE - Muestra la estructura (igual que PostgreSQL)
→ .fetchdf() - Devuelve los resultados como DataFrame de Pandas (muy útil!)

# Conectar a DuckDB (en memoria - los datos se pierden al cerrar)
con = duckdb.connect()

# DuckDB puede leer JSON o Parquet
con.execute()


## Preguntas
1. EXPLORACIÓN INICIAL
→ ¿Cuántos registros? ¿Qué período cubren?

2. ENDPOINTS MÁS USADOS
→ ¿Qué endpoints reciben más tráfico

3. ANÁLISIS DE ERRORES
→ ¿Qué endpoints tienen más errores 500

4. PERFORMANCE POR ENDPOINT
→ ¿Qué endpoints son más lentos?

5. TENDENCIA HORARIA
→ ¿A qué hora hay más tráfico?

6. WINDOW FUNCTIONS - RANKING
→ Top 3 requests más lentas por endpoint

7. COMPARACIÓN CON PERÍODO ANTERIOR
→ ¿Cómo cambia el tráfico día a día?

## Output
- `load_logs_access_logs.py`: Consulta de la tabla de access_logs (1000 registros) y respuestas a preguntas.
- `load_logs_error_logs.py`: Consulta de la tabla de error_logs
- `load_logs_services_logs.py`: Consulta de la tabla de services_logs


## Autor
Guillermo - 13/03/2026

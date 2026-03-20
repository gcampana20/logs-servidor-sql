
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
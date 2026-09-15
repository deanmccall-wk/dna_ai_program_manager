-- int_redshift_scan_classified: join scans to objects, classify users.
-- User categories:
--   system:             rdsdb, redshift, awsuser (Redshift internals)
--   dna_team:           Dean McCall's org (platform management, not consumption)
--   infosec:            service_security (runs until cluster off)
--   mv_refresh_spectrum: datasciadmin scanning S3 for MV refresh
--   mv_refresh_local:   datasciadmin scanning MV local storage for refresh
--   consumer:           everyone else (actual data consumers)

{{
    config(
        materialized='incremental',
        unique_key=['scan_date', 'perm_table_name', 'username'],
        tags=['silver']
    )
}}

WITH dna_team AS (
    SELECT
        LOWER(REPLACE(REPLACE(primary_email_address, '@workiva.com', ''), '.', '')) AS username_base
    FROM {{ source('marts', 'dim_workers') }}
    WHERE is_latest = TRUE
      AND is_active = TRUE
      AND (
          manager_1 ILIKE '%Dean McCall%'
          OR manager_2 ILIKE '%Dean McCall%'
          OR manager_3 ILIKE '%Dean McCall%'
          OR primary_email_address ILIKE 'dean.mccall@workiva.com'
      )
)

SELECT
    s.scan_date,
    s.perm_table_name,
    COALESCE(i.schema_name, 'unknown') AS schema_name,
    COALESCE(i.object_name, s.perm_table_name) AS object_name,
    COALESCE(i.object_type, 'unknown') AS object_type,
    s.username,
    s.distinct_queries,
    s.total_scans,
    s.rows_scanned,
    s.bytes_scanned,
    s.spectrum_bytes,
    s.compute_seconds,
    CASE
        WHEN s.username IN ('rdsdb', 'redshift', 'awsuser')
            THEN 'system'
        WHEN LOWER(s.username) IN (SELECT username_base FROM dna_team)
            OR LOWER(s.username) IN (SELECT username_base || '_admin' FROM dna_team)
            OR LOWER(s.username) IN (
                SELECT LOWER(primary_email_address)
                FROM {{ source('marts', 'dim_workers') }}
                WHERE is_latest = TRUE AND is_active = TRUE
                  AND (manager_1 ILIKE '%Dean McCall%' OR manager_2 ILIKE '%Dean McCall%'
                       OR manager_3 ILIKE '%Dean McCall%' OR primary_email_address ILIKE 'dean.mccall@workiva.com')
            )
            THEN 'dna_team'
        WHEN s.username = 'service_security'
            THEN 'infosec'
        WHEN s.username = 'datasciadmin'
            AND i.object_type = 'materialized_view'
            AND s.perm_table_name LIKE 'S3 %'
            THEN 'mv_refresh_spectrum'
        WHEN s.username = 'datasciadmin'
            AND s.perm_table_name LIKE 'mv_tbl__%'
            THEN 'mv_refresh_local'
        ELSE 'consumer'
    END AS user_category,
    s._extracted_at
FROM {{ ref('stg_redshift_scans') }} s
LEFT JOIN {{ ref('stg_redshift_objects') }} i
    ON s.perm_table_name = i.mv_physical_name
    OR s.perm_table_name = i.object_name

{% if is_incremental() %}
WHERE s._extracted_at > (SELECT MAX(_extracted_at) FROM {{ this }})
{% endif %}

-- redshift_orphan_inventory: one row per object, classified as orphan/low_activity/active.
-- Aggregates across all scan dates and users, excluding system/DNA/refresh.

{{
    config(
        materialized='table',
        tags=['gold']
    )
}}

SELECT
    schema_name,
    object_name,
    object_type,
    SUM(CASE WHEN user_category = 'consumer' THEN distinct_queries ELSE 0 END) AS consumer_queries,
    COUNT(DISTINCT CASE WHEN user_category = 'consumer' THEN username END) AS consumer_users,
    SUM(CASE WHEN user_category IN ('mv_refresh_spectrum', 'mv_refresh_local') THEN compute_seconds ELSE 0 END) AS refresh_compute_seconds,
    SUM(CASE WHEN user_category = 'mv_refresh_spectrum' THEN spectrum_bytes ELSE 0 END) AS refresh_spectrum_bytes,
    SUM(CASE WHEN user_category = 'infosec' THEN distinct_queries ELSE 0 END) AS infosec_queries,
    SUM(CASE WHEN user_category = 'consumer' THEN compute_seconds ELSE 0 END) AS consumer_compute_seconds,
    SUM(CASE WHEN user_category = 'consumer' THEN bytes_scanned ELSE 0 END) AS consumer_bytes_scanned,
    CASE
        WHEN SUM(CASE WHEN user_category = 'consumer' THEN distinct_queries ELSE 0 END) = 0 THEN 'orphan'
        WHEN SUM(CASE WHEN user_category = 'consumer' THEN distinct_queries ELSE 0 END) <= 10 THEN 'low_activity'
        ELSE 'active'
    END AS classification,
    MIN(scan_date) AS earliest_scan,
    MAX(scan_date) AS latest_scan,
    LISTAGG(DISTINCT CASE WHEN user_category = 'consumer' THEN username END, ', ') AS consumer_user_list
FROM {{ ref('int_redshift_scan_classified') }}
GROUP BY 1, 2, 3

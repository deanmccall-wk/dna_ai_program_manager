-- redshift_mv_prioritization: materialized views ranked by wasted compute.
-- Orphaned MVs with the highest refresh cost should be stopped first.

{{
    config(
        materialized='table',
        tags=['gold']
    )
}}

SELECT
    schema_name,
    object_name,
    classification,
    consumer_queries,
    consumer_users,
    consumer_user_list,
    infosec_queries,
    refresh_compute_seconds,
    ROUND(refresh_compute_seconds / 3600.0, 1) AS refresh_compute_hours,
    refresh_spectrum_bytes,
    ROUND(refresh_spectrum_bytes / 1e12 * 5.0, 2) AS est_spectrum_cost_usd,
    earliest_scan,
    latest_scan,
    ROW_NUMBER() OVER (ORDER BY refresh_compute_seconds DESC) AS cost_rank
FROM {{ ref('redshift_orphan_inventory') }}
WHERE object_type = 'materialized_view'
ORDER BY refresh_compute_seconds DESC

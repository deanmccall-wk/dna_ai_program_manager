-- stg_redshift_scans: dedup overlapping extracts.
-- Same (scan_date, perm_table_name, username) from multiple runs produces identical aggregates.
-- Keep the latest extract per key.

{{
    config(
        materialized='incremental',
        unique_key=['scan_date', 'perm_table_name', 'username'],
        tags=['bronze']
    )
}}

SELECT
    raw_data:scan_date::date AS scan_date,
    raw_data:perm_table_name::varchar AS perm_table_name,
    raw_data:username::varchar AS username,
    raw_data:distinct_queries::integer AS distinct_queries,
    raw_data:total_scans::integer AS total_scans,
    raw_data:rows_scanned::bigint AS rows_scanned,
    raw_data:bytes_scanned::bigint AS bytes_scanned,
    raw_data:spectrum_bytes::bigint AS spectrum_bytes,
    raw_data:compute_seconds::float AS compute_seconds,
    _extracted_at
FROM {{ source('data_platform', 'raw_redshift_scans') }}

{% if is_incremental() %}
WHERE _extracted_at > (SELECT MAX(_extracted_at) FROM {{ this }})
{% endif %}

QUALIFY ROW_NUMBER() OVER (
    PARTITION BY raw_data:scan_date::date, raw_data:perm_table_name::varchar, raw_data:username::varchar
    ORDER BY _extracted_at DESC
) = 1

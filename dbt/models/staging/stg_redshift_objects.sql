-- stg_redshift_objects: latest object inventory snapshot.

{{
    config(
        materialized='table',
        tags=['bronze']
    )
}}

SELECT
    raw_data:schemaname::varchar AS schema_name,
    raw_data:objectname::varchar AS object_name,
    raw_data:obj_type::varchar AS object_type,
    raw_data:mv_physical_name::varchar AS mv_physical_name,
    CASE
        WHEN raw_data:schemaname::varchar LIKE 'staging_%' THEN 'fivetran'
        WHEN raw_data:schemaname::varchar IN ('fivetran_log', 'fivetran_metadata') THEN 'fivetran'
        WHEN raw_data:schemaname::varchar = 'pg_s3' THEN 'spectrum_external'
        WHEN raw_data:obj_type::varchar = 'materialized_view'
            AND raw_data:schemaname::varchar = 'mv_spectrum' THEN 'spectrum_mv'
        WHEN raw_data:schemaname::varchar = 'mv_spectrum'
            AND raw_data:obj_type::varchar = 'table' THEN 'spectrum_mv_storage'
        WHEN raw_data:schemaname::varchar = 'pg_automv' THEN 'auto_mv'
        WHEN raw_data:obj_type::varchar = 'view' THEN 'derived_view'
        WHEN raw_data:schemaname::varchar IN (
            'data_mart', 'data_mart_beta', 'data_mart_sensitive', 'intermediate'
        ) THEN 'dbt_transform'
        ELSE 'overlord'
    END AS load_mechanism,
    CASE
        WHEN raw_data:schemaname::varchar LIKE 'staging_%' THEN TRUE
        WHEN raw_data:schemaname::varchar IN ('fivetran_log', 'fivetran_metadata') THEN TRUE
        WHEN raw_data:schemaname::varchar = 'pg_s3' THEN TRUE
        WHEN raw_data:obj_type::varchar = 'materialized_view'
            AND raw_data:schemaname::varchar = 'mv_spectrum' THEN TRUE
        WHEN raw_data:obj_type::varchar = 'view' THEN FALSE
        WHEN raw_data:schemaname::varchar IN (
            'data_mart', 'data_mart_beta', 'data_mart_sensitive',
            'intermediate', 'pg_automv'
        ) THEN FALSE
        WHEN raw_data:schemaname::varchar = 'mv_spectrum'
            AND raw_data:obj_type::varchar = 'table' THEN FALSE
        ELSE TRUE
    END AS is_landing_table,
    _extracted_at
FROM {{ source('data_platform', 'raw_redshift_objects') }}
WHERE _extracted_at = (SELECT MAX(_extracted_at) FROM {{ source('data_platform', 'raw_redshift_objects') }})

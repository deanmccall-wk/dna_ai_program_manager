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
    _extracted_at
FROM {{ source('data_platform', 'raw_redshift_objects') }}
WHERE _extracted_at = (SELECT MAX(_extracted_at) FROM {{ source('data_platform', 'raw_redshift_objects') }})

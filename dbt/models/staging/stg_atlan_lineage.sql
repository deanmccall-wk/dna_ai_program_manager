-- stg_atlan_lineage: deduped lineage edges from Atlan API.

{{
    config(
        materialized='table'
    )
}}

SELECT
    raw_data:source_guid::varchar AS source_guid,
    raw_data:target_guid::varchar AS target_guid,
    raw_data:source_name::varchar AS source_name,
    raw_data:target_name::varchar AS target_name,
    raw_data:source_schema::varchar AS source_schema,
    raw_data:target_schema::varchar AS target_schema,
    raw_data:source_type::varchar AS source_type,
    raw_data:target_type::varchar AS target_type,
    raw_data:source_connector::varchar AS source_connector,
    raw_data:target_connector::varchar AS target_connector,
    raw_data:source_qualified_name::varchar AS source_qualified_name,
    raw_data:target_qualified_name::varchar AS target_qualified_name,
    raw_data:root_guid::varchar AS root_guid,
    raw_data:root_name::varchar AS root_name,
    raw_data:root_schema::varchar AS root_schema,
    _extracted_at
FROM {{ source('data_platform', 'raw_atlan_lineage') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY source_guid, target_guid, root_guid
    ORDER BY _extracted_at DESC
) = 1

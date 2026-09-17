-- redshift_dependency_graph: one row per non-process lineage edge.
-- Answers: what depends on X, what feeds X, which landing tables feed QuickSight, etc.

{{
    config(
        materialized='table'
    )
}}

SELECT DISTINCT
    source_name,
    source_schema,
    source_type,
    source_connector,
    target_name,
    target_schema,
    target_type,
    target_connector,
    root_name,
    root_schema
FROM {{ ref('stg_atlan_lineage') }}
WHERE source_name IS NOT NULL
  AND target_name IS NOT NULL
  AND source_type IN ('Table', 'View', 'MaterialisedView', 'DbtModel', 'DbtSource', 'QuickSightDataset')
  AND target_type IN ('Table', 'View', 'MaterialisedView', 'DbtModel', 'DbtSource', 'QuickSightDataset')
ORDER BY root_schema, root_name, source_name

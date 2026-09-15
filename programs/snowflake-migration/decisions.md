# Decisions

| Date | Decision | Rationale | Decided by |
|------|----------|-----------|------------|
| 2026-09-15 | Phased Redshift shutdown: quick wins first, then MV migration, cluster resize (5 to 2 nodes), then full decommission after OpenAir clears | Cost-priority ordering. Cluster is 5x ra3.16xlarge ($1,267/day compute). Individual pipeline shutdowns don't reduce fixed cost -- savings come from enabling resize and shutdown. MV refreshes (375 hrs/wk) are the biggest compute consumer, not Fivetran or dbt. | Dean McCall |
| 2026-09-15 | Pause (not delete) 16 duplicated Fivetran connectors targeting Redshift | All 16 have active equivalents in Snowflake (BT_FIVETRAN_PROD). Pause is reversible. Saves ~$2.7K/mo Fivetran MAR + reduces Spectrum cost. | Dean McCall |

# Redshift Shutdown - Consumer Cutover

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Type:** Epic
**Jira:** draft

## Description

Parent epic for all work required to shut down the Redshift cluster. All data has been migrated to Snowflake. The remaining work is disabling or re-pointing the automated consumers that still read from Redshift, then resizing and terminating the cluster.

**Target:** $0 Redshift spend by November 1, 2026
**Current cost:** $1,556/day ($47K/month)

## Children

See individual tickets below, organized by phase.

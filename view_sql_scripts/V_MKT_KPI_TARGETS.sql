-- RBK_DW_DB.SA_CAMPAIGN.V_MKT_KPI_TARGETS Comparison Queries (PROD vs UAT)

-- Row Count Comparison
SELECT COUNT(*) AS count, 'PROD' AS ENV FROM RBK_DW_DB.SA_CAMPAIGN.V_MKT_KPI_TARGETS
UNION ALL
SELECT COUNT(*) AS count, 'UAT' AS ENV FROM UAT_RBK_DW_DB_DB_DBT_20240927.SA_CAMPAIGN.V_MKT_KPI_TARGETS;

-- Schema Difference: PROD - UAT
SELECT column_name, data_type
FROM RBK_DW_DB.information_schema.columns
WHERE table_name = 'V_MKT_KPI_TARGETS' AND table_schema = 'SA_CAMPAIGN'
MINUS
SELECT column_name, data_type
FROM UAT_RBK_DW_DB_DB_DBT_20240927.information_schema.columns
WHERE table_name = 'V_MKT_KPI_TARGETS' AND table_schema = 'SA_CAMPAIGN';

-- Schema Difference: UAT - PROD
SELECT column_name, data_type
FROM UAT_RBK_DW_DB_DB_DBT_20240927.information_schema.columns
WHERE table_name = 'V_MKT_KPI_TARGETS' AND table_schema = 'SA_CAMPAIGN'
MINUS
SELECT column_name, data_type
FROM RBK_DW_DB.information_schema.columns
WHERE table_name = 'V_MKT_KPI_TARGETS' AND table_schema = 'SA_CAMPAIGN';

-- Data Difference: PROD - UAT
SELECT * FROM RBK_DW_DB.SA_CAMPAIGN.V_MKT_KPI_TARGETS
MINUS
SELECT * FROM UAT_RBK_DW_DB_DB_DBT_20240927.SA_CAMPAIGN.V_MKT_KPI_TARGETS;

-- Data Difference: UAT - PROD
SELECT * FROM UAT_RBK_DW_DB_DB_DBT_20240927.SA_CAMPAIGN.V_MKT_KPI_TARGETS
MINUS
SELECT * FROM RBK_DW_DB.SA_CAMPAIGN.V_MKT_KPI_TARGETS;


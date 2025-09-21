-- RBK_DW_DB.FA_SALES.V_RPT_PIPELINE_PROJECTION_SS Comparison Queries (PROD vs DEV)

-- Column Comparison
SELECT
    a.column_name AS PROD_COLUMNS,
    a.data_type AS PROD_DATATYPE,
    b.column_name AS DEV_COLUMNS,
    b.data_type AS DEV_DATATYPE
FROM
    RBK_DW_DB.information_schema.columns a
JOIN
    DEV_RBK_DW_DB_DB_DBT20240903.information_schema.columns b
    ON a.column_name = b.column_name
WHERE
    a.table_schema = 'FA_SALES'
    AND a.table_name = 'V_RPT_PIPELINE_PROJECTION_SS'
    AND b.table_schema = 'DBT_RC'
    AND b.table_name = 'V_RPT_PIPELINE_PROJECTION_SS'
ORDER BY a.ordinal_position;

-- Row Count Comparison
SELECT COUNT(*) AS count, 'PROD' AS ENV FROM RBK_DW_DB.FA_SALES.V_RPT_PIPELINE_PROJECTION_SS
UNION ALL
SELECT COUNT(*) AS count, 'DEV' AS ENV FROM DEV_RBK_DW_DB_DB_DBT20240903.DBT_RC.V_RPT_PIPELINE_PROJECTION_SS;

-- Schema Difference: PROD - DEV
SELECT column_name, data_type
FROM RBK_DW_DB.information_schema.columns
WHERE table_name = 'V_RPT_PIPELINE_PROJECTION_SS' AND table_schema = 'FA_SALES'
MINUS
SELECT column_name, data_type
FROM DEV_RBK_DW_DB_DB_DBT20240903.information_schema.columns
WHERE table_name = 'V_RPT_PIPELINE_PROJECTION_SS' AND table_schema = 'DBT_RC';

-- Schema Difference: DEV - PROD
SELECT column_name, data_type
FROM DEV_RBK_DW_DB_DB_DBT20240903.information_schema.columns
WHERE table_name = 'V_RPT_PIPELINE_PROJECTION_SS' AND table_schema = 'DBT_RC'
MINUS
SELECT column_name, data_type
FROM RBK_DW_DB.information_schema.columns
WHERE table_name = 'V_RPT_PIPELINE_PROJECTION_SS' AND table_schema = 'FA_SALES';

-- Data Difference: PROD - DEV
SELECT * FROM RBK_DW_DB.FA_SALES.V_RPT_PIPELINE_PROJECTION_SS
MINUS
SELECT * FROM DEV_RBK_DW_DB_DB_DBT20240903.DBT_RC.V_RPT_PIPELINE_PROJECTION_SS;

-- Data Difference: DEV - PROD
SELECT * FROM DEV_RBK_DW_DB_DB_DBT20240903.DBT_RC.V_RPT_PIPELINE_PROJECTION_SS
MINUS
SELECT * FROM RBK_DW_DB.FA_SALES.V_RPT_PIPELINE_PROJECTION_SS;


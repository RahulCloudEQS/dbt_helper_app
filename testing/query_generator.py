def generate_comparison_queries(object_name: str, comparison_type: str,
                               dev_schema="DBT_RC",
                               uat_schema="UAT_RBK_DW_DB_DBT_20240927",
                               prod_schema="SA_PIPELINE",
                               prod_db="RBK_DW_DB") -> str:
    """
    Generates testing queries for a given object and comparison type.

    Args:
        object_name (str): Table/view name (e.g., V_BOOKING_LINE_F)
        comparison_type (str): "PROD vs DEV" or "UAT vs PROD"
        dev_schema (str): DEV schema (default DBT_RC)
        uat_schema (str): UAT schema (default UAT_RBK_DW_DB_DBT_20240927)
        prod_schema (str): PROD schema (default SA_PIPELINE)
        prod_db (str): PROD database (default RBK_DW_DB)

    Returns:
        str: SQL queries as a single string
    """
    table = object_name.strip()
    queries = []

    if comparison_type == "PROD vs DEV":
        dev_table = f"{dev_schema}.{table}"
        prod_table = f"{prod_db}.{prod_schema}.{table}"

        # Row count
        queries.append(f"""-- Row Count Comparison
SELECT COUNT(*) AS count, 'PROD' AS ENV FROM {prod_table}
UNION ALL
SELECT COUNT(*) AS count, 'DEV' AS ENV FROM {dev_table};""")

        # Schema differences
        queries.append(f"""-- Schema Difference: PROD - DEV
SELECT column_name, data_type
FROM {prod_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{prod_schema}'
MINUS
SELECT column_name, data_type
FROM {dev_schema}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{dev_schema}';""")

        queries.append(f"""-- Schema Difference: DEV - PROD
SELECT column_name, data_type
FROM {dev_schema}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{dev_schema}'
MINUS
SELECT column_name, data_type
FROM {prod_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{prod_schema}';""")

        # Data differences
        queries.append(f"""-- Data Difference: PROD - DEV
SELECT * FROM {prod_table}
MINUS
SELECT * FROM {dev_table};""")

        queries.append(f"""-- Data Difference: DEV - PROD
SELECT * FROM {dev_table}
MINUS
SELECT * FROM {prod_table};""")

    elif comparison_type == "UAT vs PROD":
        uat_table = f"{uat_schema}.{table}"
        prod_table = f"{prod_db}.{prod_schema}.{table}"

        # Row count
        queries.append(f"""-- Row Count Comparison
SELECT COUNT(*) AS count, 'PROD' AS ENV FROM {prod_table}
UNION ALL
SELECT COUNT(*) AS count, 'UAT' AS ENV FROM {uat_table};""")

        # Schema differences
        queries.append(f"""-- Schema Difference: PROD - UAT
SELECT column_name, data_type
FROM {prod_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{prod_schema}'
MINUS
SELECT column_name, data_type
FROM {uat_schema}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{uat_schema}';""")

        queries.append(f"""-- Schema Difference: UAT - PROD
SELECT column_name, data_type
FROM {uat_schema}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{uat_schema}'
MINUS
SELECT column_name, data_type
FROM {prod_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{prod_schema}';""")

        # Data differences
        queries.append(f"""-- Data Difference: PROD - UAT
SELECT * FROM {prod_table}
MINUS
SELECT * FROM {uat_table};""")

        queries.append(f"""-- Data Difference: UAT - PROD
SELECT * FROM {uat_table}
MINUS
SELECT * FROM {prod_table};""")

    return "\n\n".join(queries)

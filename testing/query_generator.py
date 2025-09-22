def generate_comparison_queries(object_name: str, comparison_type: str,
                                dev_db = "DEV_RBK_DW_DB_DBT20240903",
                                dev_schema="DBT_RC",
                                uat_schema="UAT_RBK_DW_DB_DBT_20240927",
                                prod_schema="SA_PIPELINE",
                                prod_db="RBK_DW_DB") -> str:
    """
    Generates testing queries for a given object and comparison type.
    object_name should be fully qualified: DB.SCHEMA.TABLE
    """
    parts = object_name.split(".")
    if len(parts) == 3:
        obj_db, obj_schema, table = parts
    elif len(parts) == 2:
        obj_db, table = parts
        obj_schema = prod_schema
    else:
        table = parts[-1]
        obj_db = prod_db
        obj_schema = prod_schema

    queries = []

    if comparison_type == "PROD vs DEV":
        dev_table = f"{dev_db}.{dev_schema}.{table}"
        prod_table = f"{obj_db}.{obj_schema}.{table}"

        queries.append(f"""-- Row Count Comparison
SELECT COUNT(*) AS count, 'PROD' AS ENV FROM {prod_table}
UNION ALL
SELECT COUNT(*) AS count, 'DEV' AS ENV FROM {dev_table};""")

        queries.append(f"""-- Schema Difference: PROD - DEV
SELECT column_name, data_type
FROM {obj_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{obj_schema}'
MINUS
SELECT column_name, data_type
FROM {dev_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{dev_schema}';""")

        queries.append(f"""-- Schema Difference: DEV - PROD
SELECT column_name, data_type
FROM {dev_db}..information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{dev_schema}'
MINUS
SELECT column_name, data_type
FROM {obj_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{obj_schema}';""")

        queries.append(f"""-- Data Difference: PROD - DEV
SELECT * FROM {prod_table}
MINUS
SELECT * FROM {dev_table};""")

        queries.append(f"""-- Data Difference: DEV - PROD
SELECT * FROM {dev_table}
MINUS
SELECT * FROM {prod_table};""")

    elif comparison_type == "UAT vs PROD":
        uat_table = f"{uat_schema}.{obj_schema}.{table}"
        prod_table = f"{obj_db}.{obj_schema}.{table}"

        queries.append(f"""-- Row Count Comparison
SELECT COUNT(*) AS count, 'PROD' AS ENV FROM {prod_table}
UNION ALL
SELECT COUNT(*) AS count, 'UAT' AS ENV FROM {uat_table};""")

        queries.append(f"""-- Schema Difference: PROD - UAT
SELECT column_name, data_type
FROM {obj_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{obj_schema}'
MINUS
SELECT column_name, data_type
FROM {uat_schema}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{obj_schema}';""")

        queries.append(f"""-- Schema Difference: UAT - PROD
SELECT column_name, data_type
FROM {uat_schema}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{obj_schema}'
MINUS
SELECT column_name, data_type
FROM {obj_db}.information_schema.columns
WHERE table_name = '{table}' AND table_schema = '{obj_schema}';""")

        queries.append(f"""-- Data Difference: PROD - UAT
SELECT * FROM {prod_table}
MINUS
SELECT * FROM {uat_table};""")

        queries.append(f"""-- Data Difference: UAT - PROD
SELECT * FROM {uat_table}
MINUS
SELECT * FROM {prod_table};""")

    return "\n\n".join(queries)

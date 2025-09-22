import pandas as pd
import re
import snowflake.connector

def connect_snowflake(user, account, warehouse, database, schema, role):
    return snowflake.connector.connect(
        user=user,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
        authenticator="externalbrowser"
    )

def load_table_mapping(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return dict(zip(df["table"], df["source"]))
    return {}

def convert_sql_to_dbt(sql_text, table_mapping, tags):
    converted_sql = sql_text

    # Replace schema.table with source() macros
    for table, source in table_mapping.items():
        pattern = re.compile(rf"\b{table}\b", re.IGNORECASE)
        converted_sql = pattern.sub(
            rf"{{{{ source('{source}', '{table}') }}}}",
            converted_sql
        )

    # Add tags block at top
    if tags:
        tags_block = f"{{% set tags = {tags} %}}\n\n"
        converted_sql = tags_block + converted_sql

    return converted_sql

def fetch_and_convert_views(conn, views_list, table_mapping, tags):
    migrated_models = {}
    all_sources = set()

    cur = conn.cursor()

    for view in views_list:
        cur.execute(f"SHOW VIEW {view}")
        view_def = None

        try:
            cur.execute(f"SELECT GET_DDL('VIEW', '{view}')")
            row = cur.fetchone()
            if row:
                view_def = row[0]
        except Exception as e:
            view_def = f"-- ❌ Could not fetch definition for {view}: {e}"

        if view_def:
            converted = convert_sql_to_dbt(view_def, table_mapping, tags)
            migrated_models[view] = converted

    cur.close()
    return migrated_models, all_sources

import streamlit as st
import re
from converters.sql_to_jinja import convert_sql_to_jinja
from testing.query_generator import generate_comparison_queries
from helpers.migrator import (
    load_table_mapping,
    connect_snowflake,
    fetch_and_convert_views
)

# Page setup
st.set_page_config(page_title="DBT Helper", layout="wide")
st.title("🚀 DBT Helper App")

# Tabs
tab1, tab2, tab3 = st.tabs([
    "SQL → Jinja Converter",
    "Migrator",
    "Testing Queries"
])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Convert SQL to Jinja Templating")

    uploaded_file = st.file_uploader("Upload SQL File", type=["sql"])
    sql_text = st.text_area("Or paste SQL script here")

    if st.button("Convert to Jinja"):
        if uploaded_file:
            sql_text = uploaded_file.read().decode("utf-8")
        if sql_text:
            converted = convert_sql_to_jinja(sql_text)
            st.success("✅ Converted to Jinja SQL:")
            st.code(converted, language="sql")
        else:
            st.warning("⚠️ Please upload a file or paste SQL text.")

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Paste Views to Convert into dbt Models")

    # Paste multiple views
    views_input = st.text_area(
        "Paste fully qualified view names (one per line):",
        height=200,
        placeholder=(
            "RBK_DW_DB.SA_PIPELINE.V_OPPORTUNITY_LINE_F\n"
            "RBK_DW_DB.SA_PIPELINE.V_QUOTE_LINE_F\n"
            "RBK_DW_DB.FA_SALES.V_RPT_PIPELINE_PROJECTION_SS"
        )
    )

    # Tags
    tags_multi = st.multiselect(
        "Add Tags (Optional)",
        ["finance", "salesforce", "etl", "incremental", "snapshot"]
    )

    # Optional table mapping CSV
    table_mapping_file = st.file_uploader("Upload table_mapping.csv (Optional)", type=["csv"])
    table_mapping = load_table_mapping(table_mapping_file)

    if st.button("🚀 Migrate Views from Snowflake"):
        views_list = [v.strip() for v in re.split(r"[\n]+", views_input) if v.strip()]

        if not views_list:
            st.warning("⚠️ Please paste at least one view name.")
        else:
            try:
                conn = connect_snowflake(
                    user="RAHUL.CHOUDHARY@RUBRIK.COM",
                    account="RUBRIK-ENTERPRISE",
                    warehouse="DEV_WISDOM_WH",
                    database="RBK_DW_DB",
                    schema="COMMON",
                    role="DEV_WISDOM_DBT_RW_ROLE"
                )

                migrated_models, all_sources = fetch_and_convert_views(
                    conn, views_list, table_mapping, tags_multi
                )

                for view_name, sql in migrated_models.items():
                    st.subheader(f"✅ {view_name}")
                    st.code(sql, language="sql")

                # Download button
                st.download_button(
                    "💾 Download All dbt Models",
                    "\n\n".join(migrated_models.values()),
                    file_name="all_models.sql",
                    mime="text/sql"
                )
            except Exception as e:
                st.error(f"❌ Snowflake connection failed: {e}")

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("📊 Generate Full Testing Queries from Object Names")

    # Comparison type
    comparison_type = st.radio(
        "Select Comparison Type:",
        ["PROD vs DEV", "UAT vs PROD"]
    )

    # Mode selection
    mode = st.radio(
        "Select Mode:",
        ["Single View Query", "Multiple Views Query"]
    )

    # ---- Single View Mode ----
    if mode == "Single View Query":
        object_name = st.text_input(
            "Object Name (Fully Qualified, e.g., RBK_DW_DB.SA_PIPELINE.V_QUOTE_LINE_F)",
            key="single_object"
        )
        if st.button("🚀 Generate Query for Single View"):
            if object_name.strip():
                queries = generate_comparison_queries(object_name.strip(), comparison_type)
                st.write(f"**{object_name.strip()} ({comparison_type})**")
                st.code(queries, language="sql")
            else:
                st.warning("⚠️ Please provide fully qualified Object Name.")

    # ---- Multiple Views Mode ----
    elif mode == "Multiple Views Query":
        objects_text = st.text_area(
            "Paste all Object Names (one per line, fully qualified)",
            key="multiple_objects",
            height=200
        )

        if st.button("🚀 Generate Queries for All Views"):
            if objects_text.strip():
                object_names = [line.strip() for line in objects_text.strip().splitlines() if line.strip()]
                all_queries = []

                for obj in object_names:
                    queries = generate_comparison_queries(obj, comparison_type)
                    st.write(f"**{obj} ({comparison_type})**")
                    st.code(queries, language="sql")
                    all_queries.append(queries)

                # Option to download all queries in one file
                st.download_button(
                    "💾 Download All Testing Queries",
                    "\n\n".join(all_queries),
                    file_name="full_testing_queries.sql",
                    mime="text/sql"
                )
            else:
                st.warning("⚠️ Please paste at least one fully qualified Object Name.")

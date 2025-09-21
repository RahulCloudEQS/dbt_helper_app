import streamlit as st
from converters.sql_to_jinja import convert_sql_to_jinja
# from migrator.snowflake_migrator import migrate_view_to_dbt
from testing.query_generator import generate_comparison_queries

st.set_page_config(page_title="DBT Helper", layout="wide")
st.title("🚀 DBT Helper App")

# Tabs
tab1, tab2, tab3 = st.tabs(["SQL → Jinja Converter", "Migrator", "Testing Queries"])

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
            st.success("Converted to Jinja SQL:")
            st.code(converted, language="sql")
        else:
            st.warning("Please upload a file or paste SQL text.")

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("🔄 Snowflake → dbt Model Migrator")

    # Paste SQL text
    view_sql = st.text_area("Paste View SQL here", height=300)

    # Add tags
    tags = st.multiselect(
        "Add Tags",
        ["finance", "salesforce", "etl", "incremental", "snapshot"]
    )

    def migrate_view_to_dbt(sql_text: str, tags: list) -> str:
        """
        Converts Snowflake SQL view into dbt model.
        For now: adds tags + replaces schema.table with source().
        """
        # Simple schema → source mapping
        schema_mapping = {
            "SA_REVENUE": "revenue",
            "SA_BOOKING": "booking",
            "SA_CUSTOMER": "customer"
        }

        converted_sql = sql_text

        # Replace schema.table with source()
        import re
        for schema, source in schema_mapping.items():
            pattern = re.compile(rf"\b{schema}\.([A-Za-z0-9_]+)\b", re.IGNORECASE)
            converted_sql = pattern.sub(
                rf"{{{{ source('{source}', '\1') }}}}",
                converted_sql
            )

        # Add tags block at top
        if tags:
            tags_block = f"{{% set tags = {tags} %}}\n\n"
            converted_sql = tags_block + converted_sql

        return converted_sql

    if st.button("🚀 Migrate View"):
        if view_sql.strip():
            model_sql = migrate_view_to_dbt(view_sql, tags)
            st.success("✅ Converted dbt model:")
            st.code(model_sql, language="sql")
            
            # Download button
            st.download_button(
                "💾 Download dbt Model",
                model_sql,
                file_name="model.sql",
                mime="text/sql"
            )
        else:
            st.warning("⚠️ Please paste a SQL view definition before migrating.")


# ---------------- TAB 3 ----------------
# ---------------- TAB 3 ----------------
# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("📊 Generate Full Testing Queries from Object Names")

    # Comparison type
    comparison_type = st.radio(
        "Select Comparison Type:",
        ["PROD vs DEV", "PROD vs UAT"]
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


# ---------------- Helper function ----------------

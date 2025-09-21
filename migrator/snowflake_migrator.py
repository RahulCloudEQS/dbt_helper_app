import streamlit as st
import re

st.title("🔄 SQL to dbt Model Migrator")

st.markdown("""
Paste your **Snowflake SQL view definition** below and convert it into a **dbt model**.  
This tool replaces schema.table references with `source()` macros.
""")

# Input box for SQL text
sql_input = st.text_area("Paste your SQL view definition here:", height=300)

# Schema → dbt source mapping (extend as needed)
schema_mapping = {
    "SA_REVENUE": "revenue",
    "SA_BOOKING": "booking",
    "SA_CUSTOMER": "customer"
}

def convert_to_dbt_model(sql_text: str) -> str:
    """
    Converts Snowflake SQL into dbt model by replacing schema.table with source().
    """
    converted_sql = sql_text

    for schema, source in schema_mapping.items():
        pattern = re.compile(rf"\b{schema}\.([A-Za-z0-9_]+)\b", re.IGNORECASE)
        converted_sql = pattern.sub(
            rf"{{{{ source('{source}', '\1') }}}}",
            converted_sql
        )

    return converted_sql

# Button to run conversion
if st.button("🚀 Convert to dbt Model"):
    if sql_input.strip():
        converted = convert_to_dbt_model(sql_input)
        
        st.subheader("✅ Converted dbt Model")
        st.code(converted, language="sql")

        # Download option
        st.download_button(
            "💾 Download dbt Model",
            converted,
            file_name="model.sql",
            mime="text/sql"
        )
    else:
        st.warning("⚠️ Please paste a SQL view definition before converting.")

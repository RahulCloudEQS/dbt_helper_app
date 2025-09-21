import re
import sqlparse

def convert_sql_to_jinja(sql_text: str) -> str:
    """
    Convert raw SQL to dbt-compatible Jinja SQL.
    Replace schema.table with {{ ref('table') }} or {{ source() }} logic.
    """

    # Replace schema.table.table → ref(table)
    pattern = re.compile(r'([A-Z0-9_]+)\.([A-Z0-9_]+)\.([A-Z0-9_]+)', re.IGNORECASE)

    def replacer(match):
        table = match.group(3).lower()
        return f"{{{{ ref('{table}') }}}}"

    converted = pattern.sub(replacer, sql_text)

    # Format SQL
    formatted = sqlparse.format(
        converted,
        keyword_case="upper",   # Uppercase SQL keywords
        identifier_case="lower", # Lowercase table/column names
        reindent=True,           # Add proper indentation
        indent_width=4
    )

    return formatted

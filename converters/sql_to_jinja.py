import re
import sqlparse

def convert_sql_to_jinja(sql_text: str) -> str:
    """
    Convert raw SQL to dbt-compatible Jinja SQL.
    Replace schema.table.table with {{ source('schema', 'table') }}.
    """

    # Pattern to match schema.database.table or schema.table.table
    pattern = re.compile(r'([A-Z0-9_]+)\.([A-Z0-9_]+)\.([A-Z0-9_]+)', re.IGNORECASE)

    def replacer(match):
        schema = match.group(2).lower()
        table = match.group(3).lower()
        return f"{{{{ source('{schema}', '{table}') }}}}"

    converted = pattern.sub(replacer, sql_text)

    # Format SQL
    formatted = sqlparse.format(
        converted,
        keyword_case="lower",   # Uppercase SQL keywords
        identifier_case="lower", # Lowercase table/column names
        reindent=True,           # Add proper indentation
        indent_width=4
    )

    return formatted

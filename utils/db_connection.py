import snowflake.connector

def get_snowflake_connection(account, user, warehouse, database, schema, role=None):
    """
    Connects to Snowflake using External Browser Authentication (SSO).
    """
    conn = snowflake.connector.connect(
        user=user,
        account=account,
        authenticator="externalbrowser",  # Open SSO in browser
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role
    )
    return conn

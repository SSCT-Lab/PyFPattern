def get_schema_info(cursor, schema):
    query = ("SELECT schema_owner AS owner FROM information_schema.schemata WHERE schema_name = '%s'" % schema)
    cursor.execute(query)
    return cursor.fetchone()
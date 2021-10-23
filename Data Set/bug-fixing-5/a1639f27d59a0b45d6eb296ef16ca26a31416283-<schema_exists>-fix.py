def schema_exists(cursor, schema):
    query = ("SELECT schema_name FROM information_schema.schemata WHERE schema_name = '%s'" % schema)
    cursor.execute(query)
    return (cursor.rowcount == 1)
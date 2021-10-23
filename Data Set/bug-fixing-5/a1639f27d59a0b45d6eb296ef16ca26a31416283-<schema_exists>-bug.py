def schema_exists(cursor, schema):
    query = 'SELECT schema_name FROM information_schema.schemata WHERE schema_name = %(schema)s'
    cursor.execute(query, {
        'schema': schema,
    })
    return (cursor.rowcount == 1)
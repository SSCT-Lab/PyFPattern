def get_schema_info(cursor, schema):
    query = '\n    SELECT schema_owner AS owner\n    FROM information_schema.schemata\n    WHERE schema_name = %(schema)s\n    '
    cursor.execute(query, {
        'schema': schema,
    })
    return cursor.fetchone()
def schema_delete(cursor, schema, cascade):
    if schema_exists(cursor, schema):
        query = ('DROP SCHEMA %s' % pg_quote_identifier(schema, 'schema'))
        if cascade:
            query += ' CASCADE'
        cursor.execute(query)
        return True
    else:
        return False
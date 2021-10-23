def schema_create(cursor, schema, owner):
    if (not schema_exists(cursor, schema)):
        query_fragments = [('CREATE SCHEMA %s' % pg_quote_identifier(schema, 'schema'))]
        if owner:
            query_fragments.append(('AUTHORIZATION %s' % pg_quote_identifier(owner, 'role')))
        query = ' '.join(query_fragments)
        cursor.execute(query)
        executed_queries.append(query)
        return True
    else:
        schema_info = get_schema_info(cursor, schema)
        if (owner and (owner != schema_info['owner'])):
            return set_owner(cursor, schema, owner)
        else:
            return False
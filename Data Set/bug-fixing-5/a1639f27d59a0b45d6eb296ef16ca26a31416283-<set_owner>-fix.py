def set_owner(cursor, schema, owner):
    query = ('ALTER SCHEMA %s OWNER TO %s' % (pg_quote_identifier(schema, 'schema'), pg_quote_identifier(owner, 'role')))
    cursor.execute(query)
    executed_queries.append(query)
    return True
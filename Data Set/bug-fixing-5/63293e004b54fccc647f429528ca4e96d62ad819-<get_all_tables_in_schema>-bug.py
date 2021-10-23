def get_all_tables_in_schema(self, schema):
    if (not self.schema_exists(schema)):
        raise Error(('Schema "%s" does not exist.' % schema))
    query = "SELECT relname\n                   FROM pg_catalog.pg_class c\n                   JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace\n                   WHERE nspname = %s AND relkind in ('r', 'v', 'm')"
    self.cursor.execute(query, (schema,))
    return [t[0] for t in self.cursor.fetchall()]
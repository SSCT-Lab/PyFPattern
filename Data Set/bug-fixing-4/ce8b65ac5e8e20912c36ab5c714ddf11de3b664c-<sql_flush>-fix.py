def sql_flush(self, style, tables, sequences, allow_cascade=False):
    if (tables and allow_cascade):
        query = ('\n            WITH tables AS (\n                %s\n                UNION\n                SELECT sqlite_master.name\n                FROM sqlite_master\n                JOIN tables ON (\n                    sql REGEXP %%s || tables.name || %%s\n                )\n            ) SELECT name FROM tables;\n            ' % ' UNION '.join((("SELECT '%s' name" % table) for table in tables)))
        params = ('(?i)\\s+references\\s+("|\\\')?', '("|\\\')?\\s*\\(')
        with self.connection.cursor() as cursor:
            results = cursor.execute(query, params)
            tables = [row[0] for row in results.fetchall()]
    sql = [('%s %s %s;' % (style.SQL_KEYWORD('DELETE'), style.SQL_KEYWORD('FROM'), style.SQL_FIELD(self.quote_name(table)))) for table in tables]
    return sql
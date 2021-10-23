def sql_flush(self, style, tables, sequences, allow_cascade=False):
    sql = [('%s %s %s;' % (style.SQL_KEYWORD('DELETE'), style.SQL_KEYWORD('FROM'), style.SQL_FIELD(self.quote_name(table)))) for table in tables]
    return sql
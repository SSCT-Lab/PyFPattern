def last_insert_id(self, cursor, table_name, pk_name):
    sq_name = self._get_sequence_name(table_name)
    cursor.execute(('"%s".currval' % sq_name))
    return cursor.fetchone()[0]
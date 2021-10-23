def connect(self):
    'Connect to a PostgreSQL database and return a cursor object.\n\n        Note: connection parameters are passed by self.module object.\n        '
    self.db_conn = connect_to_db(self.module, warn_db_default=False)
    return self.db_conn.cursor(cursor_factory=DictCursor)
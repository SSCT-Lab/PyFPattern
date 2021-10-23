def reconnect(self, dbname):
    'Reconnect to another database and return a PostgreSQL cursor object.\n\n        Arguments:\n            dbname (string): Database name to connect to.\n        '
    self.db_conn.close()
    self.module.params['database'] = dbname
    return self.connect()
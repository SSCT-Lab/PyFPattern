def reconnect(self, dbname):
    self.db_conn.close()
    self.module.params['database'] = dbname
    return self.connect()
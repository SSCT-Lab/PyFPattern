def get_pg_version(self):
    query = 'SELECT version()'
    raw = self.__exec_sql(query)[0][0]
    raw = raw.split()[1].split('.')
    self.pg_info['version'] = dict(major=int(raw[0]), minor=int(raw[1]))
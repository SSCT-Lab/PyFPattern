def get_db_info(self):
    query = "SELECT d.datname, pg_catalog.pg_get_userbyid(d.datdba), pg_catalog.pg_encoding_to_char(d.encoding), d.datcollate, d.datctype, pg_catalog.array_to_string(d.datacl, E'\n'), CASE WHEN pg_catalog.has_database_privilege(d.datname, 'CONNECT') THEN pg_catalog.pg_database_size(d.datname)::text ELSE 'No Access' END, t.spcname FROM pg_catalog.pg_database AS d JOIN pg_catalog.pg_tablespace t ON d.dattablespace = t.oid WHERE d.datname != 'template0'"
    res = self.__exec_sql(query)
    db_dict = {
        
    }
    for i in res:
        db_dict[i[0]] = dict(owner=i[1], encoding=i[2], collate=i[3], ctype=i[4], access_priv=(i[5] if i[5] else ''), size=i[6])
    for datname in db_dict:
        self.cursor = self.db_obj.reconnect(datname)
        db_dict[datname]['namespaces'] = self.get_namespaces()
        db_dict[datname]['extensions'] = self.get_ext_info()
        db_dict[datname]['languages'] = self.get_lang_info()
    self.pg_info['databases'] = db_dict
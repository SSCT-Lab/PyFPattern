def __exec_sql(self, query):
    try:
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        if res:
            return res
    except Exception as e:
        self.module.fail_json(msg=("Cannot execute SQL '%s': %s" % (query, to_native(e))))
        self.cursor.close()
    return False
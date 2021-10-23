def connect(self):
    try:
        self.db_conn = connect_to_db(self.module, warn_db_default=False)
        self.cursor = self.db_conn.cursor(cursor_factory=DictCursor)
        if self.session_role:
            try:
                self.cursor.execute(('SET ROLE %s' % self.session_role))
            except Exception as e:
                self.module.fail_json(msg=('Could not switch role: %s' % to_native(e)))
        return self.cursor
    except TypeError as e:
        if ('sslrootcert' in e.args[0]):
            self.module.fail_json(msg='PostgreSQL server must be at least version 8.4 to support sslrootcert')
        self.module.fail_json(msg=('Unable to connect to database: %s' % to_native(e)))
    except Exception as e:
        self.module.fail_json(msg=('Unable to connect to database: %s' % to_native(e)))
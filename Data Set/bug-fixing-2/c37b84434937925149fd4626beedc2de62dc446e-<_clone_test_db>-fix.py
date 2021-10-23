

def _clone_test_db(self, suffix, verbosity, keepdb=False):
    source_database_name = self.connection.settings_dict['NAME']
    target_database_name = self.get_test_db_clone_settings(suffix)['NAME']
    test_db_params = {
        'dbname': self.connection.ops.quote_name(target_database_name),
        'suffix': self.sql_table_creation_suffix(),
    }
    with self._nodb_connection.cursor() as cursor:
        try:
            self._execute_create_test_db(cursor, test_db_params, keepdb)
        except Exception:
            try:
                if (verbosity >= 1):
                    self.log(('Destroying old test database for alias %s…' % (self._get_database_display_str(verbosity, target_database_name),)))
                cursor.execute(('DROP DATABASE %(dbname)s' % test_db_params))
                self._execute_create_test_db(cursor, test_db_params, keepdb)
            except Exception as e:
                self.log(('Got an error recreating the test database: %s' % e))
                sys.exit(2)
    dump_cmd = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)
    dump_cmd[0] = 'mysqldump'
    dump_cmd[(- 1)] = source_database_name
    load_cmd = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)
    load_cmd[(- 1)] = target_database_name
    with subprocess.Popen(dump_cmd, stdout=subprocess.PIPE) as dump_proc:
        with subprocess.Popen(load_cmd, stdin=dump_proc.stdout, stdout=subprocess.DEVNULL):
            dump_proc.stdout.close()

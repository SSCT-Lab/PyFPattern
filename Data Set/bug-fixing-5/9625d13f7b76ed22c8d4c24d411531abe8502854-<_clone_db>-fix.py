def _clone_db(self, source_database_name, target_database_name):
    dump_args = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)[1:]
    dump_args[(- 1)] = source_database_name
    dump_cmd = (['mysqldump', '--routines', '--events'] + dump_args)
    load_cmd = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)
    load_cmd[(- 1)] = target_database_name
    with subprocess.Popen(dump_cmd, stdout=subprocess.PIPE) as dump_proc:
        with subprocess.Popen(load_cmd, stdin=dump_proc.stdout, stdout=subprocess.DEVNULL):
            dump_proc.stdout.close()
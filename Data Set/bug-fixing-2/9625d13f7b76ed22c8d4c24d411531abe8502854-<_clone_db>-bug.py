

def _clone_db(self, source_database_name, target_database_name):
    dump_cmd = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)
    dump_cmd[0] = 'mysqldump'
    dump_cmd[(- 1)] = source_database_name
    load_cmd = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)
    load_cmd[(- 1)] = target_database_name
    with subprocess.Popen(dump_cmd, stdout=subprocess.PIPE) as dump_proc:
        with subprocess.Popen(load_cmd, stdin=dump_proc.stdout, stdout=subprocess.DEVNULL):
            dump_proc.stdout.close()

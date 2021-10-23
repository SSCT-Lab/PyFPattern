

def execute(self, context):
    '\n        Execute the bash command in a temporary directory\n        which will be cleaned afterwards\n        '
    self.log.info('Tmp dir root location: \n %s', gettempdir())
    if (self.env is None):
        self.env = os.environ.copy()
    airflow_context_vars = context_to_airflow_vars(context, in_env_var_format=True)
    self.log.info('Exporting the following env vars:\n%s', '\n'.join(['{}={}'.format(k, v) for (k, v) in airflow_context_vars.items()]))
    self.env.update(airflow_context_vars)
    self.lineage_data = self.bash_command
    with TemporaryDirectory(prefix='airflowtmp') as tmp_dir:
        with NamedTemporaryFile(dir=tmp_dir, prefix=self.task_id) as tmp_file:
            tmp_file.write(bytes(self.bash_command, 'utf_8'))
            tmp_file.flush()
            script_location = os.path.abspath(tmp_file.name)
            self.log.info('Temporary script location: %s', script_location)

            def pre_exec():
                for sig in ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ'):
                    if hasattr(signal, sig):
                        signal.signal(getattr(signal, sig), signal.SIG_DFL)
                os.setsid()
            self.log.info('Running command: %s', self.bash_command)
            sub_process = Popen(['bash', tmp_file.name], stdout=PIPE, stderr=STDOUT, cwd=tmp_dir, env=self.env, preexec_fn=pre_exec)
            self.sub_process = sub_process
            self.log.info('Output:')
            line = ''
            for raw_line in iter(sub_process.stdout.readline, b''):
                line = raw_line.decode(self.output_encoding).rstrip()
                self.log.info(line)
            sub_process.wait()
            self.log.info('Command exited with return code %s', sub_process.returncode)
            if sub_process.returncode:
                raise AirflowException('Bash command failed')
    return line

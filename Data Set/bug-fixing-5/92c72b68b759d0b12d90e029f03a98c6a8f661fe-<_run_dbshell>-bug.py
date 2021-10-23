def _run_dbshell(self, rlwrap=False):
    'Run runshell command and capture its arguments.'

    def _mock_subprocess_run(*args):
        self.subprocess_args = list(*args)
        return CompletedProcess(self.subprocess_args, 0)
    client = DatabaseClient(connection)
    self.subprocess_args = None
    with mock.patch('subprocess.run', new=_mock_subprocess_run):
        with mock.patch('shutil.which', return_value=('/usr/bin/rlwrap' if rlwrap else None)):
            client.runshell()
    return self.subprocess_args
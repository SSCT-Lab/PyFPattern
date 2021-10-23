def test_with_rlwrap(self):
    self.assertEqual(self._run_dbshell(rlwrap=True), ('/usr/bin/rlwrap', 'sqlplus', '-L', connection._connect_string()))
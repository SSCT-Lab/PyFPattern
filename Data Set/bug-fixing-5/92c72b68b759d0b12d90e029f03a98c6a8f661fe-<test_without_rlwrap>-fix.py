def test_without_rlwrap(self):
    self.assertEqual(self._run_dbshell(rlwrap=False), ['sqlplus', '-L', connection._connect_string()])
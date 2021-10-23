def test_notafile_error(self):
    with self.assertRaises((PermissionError if sys.platform.startswith('win') else IsADirectoryError)):
        self.engine.get_template('first')
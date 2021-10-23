def test_notafile_error(self):
    with self.assertRaises(IsADirectoryError):
        self.engine.get_template('first')
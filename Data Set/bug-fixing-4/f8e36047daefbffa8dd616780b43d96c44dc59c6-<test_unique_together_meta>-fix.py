def test_unique_together_meta(self):
    out = StringIO()
    call_command('inspectdb', 'inspectdb_uniquetogether', stdout=out)
    output = out.getvalue()
    unique_re = re.compile('.*unique_together = \\((.+),\\).*')
    unique_together_match = re.findall(unique_re, output)
    self.assertEqual(len(unique_together_match), 1)
    fields = unique_together_match[0]
    self.assertIn("('field1', 'field2')", fields)
    self.assertIn("('field1', 'field2')", fields)
    self.assertIn("('non_unique_column', 'non_unique_column_0')", fields)
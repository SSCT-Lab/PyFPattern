def test_digits_column_name_introspection(self):
    'Introspection of column names consist/start with digits (#16536/#17676)'
    out = StringIO()
    call_command('inspectdb', table_name_filter=(lambda tn: tn.startswith('inspectdb_')), stdout=out)
    output = out.getvalue()
    error_message = 'inspectdb generated a model field name which is a number'
    self.assertNotIn('    123 = models.CharField', output, msg=error_message)
    self.assertIn('number_123 = models.CharField', output)
    error_message = 'inspectdb generated a model field name which starts with a digit'
    self.assertNotIn('    4extra = models.CharField', output, msg=error_message)
    self.assertIn('number_4extra = models.CharField', output)
    self.assertNotIn('    45extra = models.CharField', output, msg=error_message)
    self.assertIn('number_45extra = models.CharField', output)
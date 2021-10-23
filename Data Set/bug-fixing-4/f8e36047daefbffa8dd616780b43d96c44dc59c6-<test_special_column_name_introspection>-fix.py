def test_special_column_name_introspection(self):
    '\n        Introspection of column names containing special characters,\n        unsuitable for Python identifiers\n        '
    out = StringIO()
    call_command('inspectdb', table_name_filter=(lambda tn: tn.startswith('inspectdb_special')), stdout=out)
    output = out.getvalue()
    base_name = ('Field' if (not connection.features.uppercases_column_names) else 'field')
    self.assertIn('field = models.IntegerField()', output)
    self.assertIn(("field_field = models.IntegerField(db_column='%s_')" % base_name), output)
    self.assertIn(("field_field_0 = models.IntegerField(db_column='%s__')" % base_name), output)
    self.assertIn("field_field_1 = models.IntegerField(db_column='__field')", output)
    self.assertIn("prc_x = models.IntegerField(db_column='prc(%) x')", output)
    if PY3:
        self.assertIn('tamaño = models.IntegerField()', output)
    else:
        self.assertIn("tama_o = models.IntegerField(db_column='tama\\xf1o')", output)
def test_table_name_introspection(self):
    '\n        Introspection of table names containing special characters,\n        unsuitable for Python identifiers\n        '
    out = StringIO()
    call_command('inspectdb', table_name_filter=(lambda tn: tn.startswith('inspectdb_')), stdout=out)
    output = out.getvalue()
    self.assertIn('class InspectdbSpecialTableName(models.Model):', output)
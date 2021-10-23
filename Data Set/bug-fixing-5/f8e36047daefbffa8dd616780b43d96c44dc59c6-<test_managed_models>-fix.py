def test_managed_models(self):
    'By default the command generates models with `Meta.managed = False` (#14305)'
    out = StringIO()
    call_command('inspectdb', 'inspectdb_columntypes', stdout=out)
    output = out.getvalue()
    self.longMessage = False
    self.assertIn('        managed = False', output, msg='inspectdb should generate unmanaged models.')
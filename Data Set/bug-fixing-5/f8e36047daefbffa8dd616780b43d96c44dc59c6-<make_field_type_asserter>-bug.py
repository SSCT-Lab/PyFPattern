def make_field_type_asserter(self):
    'Call inspectdb and return a function to validate a field type in its output'
    out = StringIO()
    call_command('inspectdb', table_name_filter=(lambda tn: tn.startswith('inspectdb_columntypes')), stdout=out)
    output = out.getvalue()

    def assertFieldType(name, definition):
        out_def = re.search(('^\\s*%s = (models.*)$' % name), output, re.MULTILINE).groups()[0]
        self.assertEqual(definition, out_def)
    return assertFieldType
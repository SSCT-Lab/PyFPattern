@skipUnless((connection.vendor == 'sqlite'), "Only patched sqlite's DatabaseIntrospection.data_types_reverse for this test")
def test_custom_fields(self):
    '\n        Introspection of columns with a custom field (#21090)\n        '
    out = StringIO()
    orig_data_types_reverse = connection.introspection.data_types_reverse
    try:
        connection.introspection.data_types_reverse = {
            'text': 'myfields.TextField',
            'bigint': 'BigIntegerField',
        }
        call_command('inspectdb', table_name_filter=(lambda tn: tn.startswith('inspectdb_columntypes')), stdout=out)
        output = out.getvalue()
        self.assertIn('text_field = myfields.TextField()', output)
        self.assertIn('big_int_field = models.BigIntegerField()', output)
    finally:
        connection.introspection.data_types_reverse = orig_data_types_reverse
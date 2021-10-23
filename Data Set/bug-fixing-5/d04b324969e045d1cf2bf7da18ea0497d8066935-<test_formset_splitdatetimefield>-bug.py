def test_formset_splitdatetimefield(self):
    '\n        Formset should also work with SplitDateTimeField(initial=datetime.datetime.now).\n        Regression test for #18709.\n        '
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-when_0': '1904-06-16',
        'form-0-when_1': '15:51:33',
    }
    formset = SplitDateTimeFormSet(data)
    self.assertTrue(formset.is_valid())
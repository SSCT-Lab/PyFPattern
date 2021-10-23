def test_formset_splitdatetimefield(self):
    '\n        Formset works with SplitDateTimeField(initial=datetime.datetime.now).\n        '

    class SplitDateTimeForm(Form):
        when = SplitDateTimeField(initial=datetime.datetime.now)
    SplitDateTimeFormSet = formset_factory(SplitDateTimeForm)
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-when_0': '1904-06-16',
        'form-0-when_1': '15:51:33',
    }
    formset = SplitDateTimeFormSet(data)
    self.assertTrue(formset.is_valid())
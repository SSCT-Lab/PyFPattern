def test_formset_nonzero(self):
    'A formsets without any forms evaluates as True.'
    ChoiceFormset = formset_factory(Choice, extra=0)
    formset = ChoiceFormset()
    self.assertEqual(len(formset.forms), 0)
    self.assertTrue(formset)
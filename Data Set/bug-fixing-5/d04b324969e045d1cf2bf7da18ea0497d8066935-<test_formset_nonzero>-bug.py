def test_formset_nonzero(self):
    '\n        Formsets with no forms should still evaluate as true.\n        Regression test for #15722\n        '
    ChoiceFormset = formset_factory(Choice, extra=0)
    formset = ChoiceFormset()
    self.assertEqual(len(formset.forms), 0)
    self.assertTrue(formset)
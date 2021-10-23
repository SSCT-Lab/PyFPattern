def test_formset_iteration(self):
    ChoiceFormset = formset_factory(Choice, extra=3)
    formset = ChoiceFormset()
    forms = list(formset)
    self.assertEqual(forms, formset.forms)
    self.assertEqual(len(formset), len(forms))
    self.assertEqual(formset[0], forms[0])
    with self.assertRaises(IndexError):
        formset[3]

    class BaseReverseFormSet(BaseFormSet):

        def __iter__(self):
            return reversed(self.forms)

        def __getitem__(self, idx):
            return super().__getitem__(((len(self) - idx) - 1))
    ReverseChoiceFormset = formset_factory(Choice, BaseReverseFormSet, extra=3)
    reverse_formset = ReverseChoiceFormset()
    self.assertEqual(str(reverse_formset[0]), str(forms[(- 1)]))
    self.assertEqual(str(reverse_formset[1]), str(forms[(- 2)]))
    self.assertEqual(len(reverse_formset), len(forms))
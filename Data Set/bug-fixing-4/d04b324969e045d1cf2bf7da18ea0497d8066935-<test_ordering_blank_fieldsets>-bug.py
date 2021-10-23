def test_ordering_blank_fieldsets(self):
    data = {
        'choices-TOTAL_FORMS': '3',
        'choices-INITIAL_FORMS': '0',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
    }
    ChoiceFormSet = formset_factory(Choice, can_order=True)
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertTrue(formset.is_valid())
    form_output = []
    for form in formset.ordered_forms:
        form_output.append(form.cleaned_data)
    self.assertEqual(form_output, [])
def test_formset_validate_min_flag(self):
    "\n        If validate_min is set and min_num is more than TOTAL_FORMS in the\n        data, a ValidationError is raised. MIN_NUM_FORMS in the data is\n        irrelevant here (it's output as a hint for the client but its value\n        in the returned data is not checked).\n        "
    data = {
        'choices-TOTAL_FORMS': '2',
        'choices-INITIAL_FORMS': '0',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
        'choices-0-choice': 'Zero',
        'choices-0-votes': '0',
        'choices-1-choice': 'One',
        'choices-1-votes': '1',
    }
    ChoiceFormSet = formset_factory(Choice, extra=1, min_num=3, validate_min=True)
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertFalse(formset.is_valid())
    self.assertEqual(formset.non_form_errors(), ['Please submit 3 or more forms.'])
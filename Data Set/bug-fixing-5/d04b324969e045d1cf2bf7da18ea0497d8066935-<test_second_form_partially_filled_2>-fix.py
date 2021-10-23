def test_second_form_partially_filled_2(self):
    'A partially completed form is invalid.'
    data = {
        'choices-TOTAL_FORMS': '3',
        'choices-INITIAL_FORMS': '0',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
        'choices-0-choice': 'Calexico',
        'choices-0-votes': '100',
        'choices-1-choice': 'The Decemberists',
        'choices-1-votes': '',
        'choices-2-choice': '',
        'choices-2-votes': '',
    }
    ChoiceFormSet = formset_factory(Choice, extra=3)
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertFalse(formset.is_valid())
    self.assertEqual(formset.errors, [{
        
    }, {
        'votes': ['This field is required.'],
    }, {
        
    }])
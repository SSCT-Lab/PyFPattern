def test_empty_ordered_fields(self):
    "\n        Ordering fields are allowed to be left blank. If they are left blank,\n        they'll be sorted below everything else.\n        "
    data = {
        'choices-TOTAL_FORMS': '4',
        'choices-INITIAL_FORMS': '3',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
        'choices-0-choice': 'Calexico',
        'choices-0-votes': '100',
        'choices-0-ORDER': '1',
        'choices-1-choice': 'Fergie',
        'choices-1-votes': '900',
        'choices-1-ORDER': '2',
        'choices-2-choice': 'The Decemberists',
        'choices-2-votes': '500',
        'choices-2-ORDER': '',
        'choices-3-choice': 'Basia Bulat',
        'choices-3-votes': '50',
        'choices-3-ORDER': '',
    }
    ChoiceFormSet = formset_factory(Choice, can_order=True)
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertTrue(formset.is_valid())
    form_output = []
    for form in formset.ordered_forms:
        form_output.append(form.cleaned_data)
    self.assertEqual(form_output, [{
        'votes': 100,
        'ORDER': 1,
        'choice': 'Calexico',
    }, {
        'votes': 900,
        'ORDER': 2,
        'choice': 'Fergie',
    }, {
        'votes': 500,
        'ORDER': None,
        'choice': 'The Decemberists',
    }, {
        'votes': 50,
        'ORDER': None,
        'choice': 'Basia Bulat',
    }])
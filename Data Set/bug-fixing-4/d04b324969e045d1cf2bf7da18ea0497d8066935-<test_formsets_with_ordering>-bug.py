def test_formsets_with_ordering(self):
    ChoiceFormSet = formset_factory(Choice, can_order=True)
    initial = [{
        'choice': 'Calexico',
        'votes': 100,
    }, {
        'choice': 'Fergie',
        'votes': 900,
    }]
    formset = ChoiceFormSet(initial=initial, auto_id=False, prefix='choices')
    form_output = []
    for form in formset.forms:
        form_output.append(form.as_ul())
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" value="Calexico" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" value="100" /></li>\n<li>Order: <input type="number" name="choices-0-ORDER" value="1" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" value="Fergie" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" value="900" /></li>\n<li>Order: <input type="number" name="choices-1-ORDER" value="2" /></li>\n<li>Choice: <input type="text" name="choices-2-choice" /></li>\n<li>Votes: <input type="number" name="choices-2-votes" /></li>\n<li>Order: <input type="number" name="choices-2-ORDER" /></li>')
    data = {
        'choices-TOTAL_FORMS': '3',
        'choices-INITIAL_FORMS': '2',
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
        'choices-2-ORDER': '0',
    }
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertTrue(formset.is_valid())
    form_output = []
    for form in formset.ordered_forms:
        form_output.append(form.cleaned_data)
    self.assertEqual(form_output, [{
        'votes': 500,
        'ORDER': 0,
        'choice': 'The Decemberists',
    }, {
        'votes': 100,
        'ORDER': 1,
        'choice': 'Calexico',
    }, {
        'votes': 900,
        'ORDER': 2,
        'choice': 'Fergie',
    }])
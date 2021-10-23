def test_formset_with_deletion(self):
    '\n        formset_factory\'s can_delete argument adds a boolean "delete" field to\n        each form. When that boolean field is True, the form will be in\n        formset.deleted_forms.\n        '
    ChoiceFormSet = formset_factory(Choice, can_delete=True)
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
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" value="Calexico" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" value="100" /></li>\n<li>Delete: <input type="checkbox" name="choices-0-DELETE" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" value="Fergie" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" value="900" /></li>\n<li>Delete: <input type="checkbox" name="choices-1-DELETE" /></li>\n<li>Choice: <input type="text" name="choices-2-choice" /></li>\n<li>Votes: <input type="number" name="choices-2-votes" /></li>\n<li>Delete: <input type="checkbox" name="choices-2-DELETE" /></li>')
    data = {
        'choices-TOTAL_FORMS': '3',
        'choices-INITIAL_FORMS': '2',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
        'choices-0-choice': 'Calexico',
        'choices-0-votes': '100',
        'choices-0-DELETE': '',
        'choices-1-choice': 'Fergie',
        'choices-1-votes': '900',
        'choices-1-DELETE': 'on',
        'choices-2-choice': '',
        'choices-2-votes': '',
        'choices-2-DELETE': '',
    }
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertTrue(formset.is_valid())
    self.assertEqual([form.cleaned_data for form in formset.forms], [{
        'votes': 100,
        'DELETE': False,
        'choice': 'Calexico',
    }, {
        'votes': 900,
        'DELETE': True,
        'choice': 'Fergie',
    }, {
        
    }])
    self.assertEqual([form.cleaned_data for form in formset.deleted_forms], [{
        'votes': 900,
        'DELETE': True,
        'choice': 'Fergie',
    }])
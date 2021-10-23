def test_more_initial_data(self):
    '\n        The extra argument works when the formset is pre-filled with initial\n        data.\n        '
    initial = [{
        'choice': 'Calexico',
        'votes': 100,
    }]
    ChoiceFormSet = formset_factory(Choice, extra=3)
    formset = ChoiceFormSet(initial=initial, auto_id=False, prefix='choices')
    form_output = []
    for form in formset.forms:
        form_output.append(form.as_ul())
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" value="Calexico" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" value="100" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" /></li>\n<li>Choice: <input type="text" name="choices-2-choice" /></li>\n<li>Votes: <input type="number" name="choices-2-votes" /></li>\n<li>Choice: <input type="text" name="choices-3-choice" /></li>\n<li>Votes: <input type="number" name="choices-3-votes" /></li>')
    self.assertTrue(formset.empty_form.empty_permitted)
    self.assertHTMLEqual(formset.empty_form.as_ul(), '<li>Choice: <input type="text" name="choices-__prefix__-choice" /></li>\n<li>Votes: <input type="number" name="choices-__prefix__-votes" /></li>')
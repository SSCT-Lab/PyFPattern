def test_formset_initial_data(self):
    '\n        A FormSet can be prefilled with existing data by providing a list of\n        dicts to the `initial` argument. By default, an extra blank form is\n        included.\n        '
    initial = [{
        'choice': 'Calexico',
        'votes': 100,
    }]
    formset = self.make_choiceformset(initial=initial)
    form_output = []
    for form in formset.forms:
        form_output.append(form.as_ul())
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" value="Calexico" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" value="100" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" /></li>')
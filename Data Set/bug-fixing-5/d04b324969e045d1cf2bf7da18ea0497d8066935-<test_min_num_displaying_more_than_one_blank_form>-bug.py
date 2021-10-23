def test_min_num_displaying_more_than_one_blank_form(self):
    ChoiceFormSet = formset_factory(Choice, extra=1, min_num=1)
    formset = ChoiceFormSet(auto_id=False, prefix='choices')
    form_output = []
    for form in formset.forms:
        form_output.append(form.as_ul())
    self.assertFalse(formset.forms[0].empty_permitted)
    self.assertTrue(formset.forms[1].empty_permitted)
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" /></li>')
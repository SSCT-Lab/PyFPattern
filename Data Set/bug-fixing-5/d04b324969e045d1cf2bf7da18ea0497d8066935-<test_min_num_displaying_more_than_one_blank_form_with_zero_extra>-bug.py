def test_min_num_displaying_more_than_one_blank_form_with_zero_extra(self):
    ChoiceFormSet = formset_factory(Choice, extra=0, min_num=3)
    formset = ChoiceFormSet(auto_id=False, prefix='choices')
    form_output = []
    for form in formset.forms:
        form_output.append(form.as_ul())
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" /></li>\n<li>Choice: <input type="text" name="choices-2-choice" /></li>\n<li>Votes: <input type="number" name="choices-2-votes" /></li>')
def test_displaying_more_than_one_blank_form(self):
    ChoiceFormSet = formset_factory(Choice, extra=3)
    formset = ChoiceFormSet(auto_id=False, prefix='choices')
    form_output = []
    for form in formset.forms:
        form_output.append(form.as_ul())
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" /></li>\n<li>Choice: <input type="text" name="choices-2-choice" /></li>\n<li>Votes: <input type="number" name="choices-2-votes" /></li>')
    data = {
        'choices-TOTAL_FORMS': '3',
        'choices-INITIAL_FORMS': '0',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
        'choices-0-choice': '',
        'choices-0-votes': '',
        'choices-1-choice': '',
        'choices-1-votes': '',
        'choices-2-choice': '',
        'choices-2-votes': '',
    }
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertTrue(formset.is_valid())
    self.assertEqual([form.cleaned_data for form in formset.forms], [{
        
    }, {
        
    }, {
        
    }])
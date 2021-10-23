def test_basic_formset(self):
    formset = self.make_choiceformset()
    self.assertHTMLEqual(str(formset), '<input type="hidden" name="choices-TOTAL_FORMS" value="1" />\n<input type="hidden" name="choices-INITIAL_FORMS" value="0" />\n<input type="hidden" name="choices-MIN_NUM_FORMS" value="0" />\n<input type="hidden" name="choices-MAX_NUM_FORMS" value="1000" />\n<tr><th>Choice:</th><td><input type="text" name="choices-0-choice" /></td></tr>\n<tr><th>Votes:</th><td><input type="number" name="choices-0-votes" /></td></tr>')
    formset = self.make_choiceformset([('Calexico', '100')])
    self.assertTrue(formset.is_valid())
    self.assertEqual([form.cleaned_data for form in formset.forms], [{
        'votes': 100,
        'choice': 'Calexico',
    }])
    formset = self.make_choiceformset()
    self.assertFalse(formset.is_valid())
    self.assertFalse(formset.has_changed())
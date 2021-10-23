def test_formset_has_changed(self):
    "\n        FormSet.has_changed() is True if any data is passed to its forms, even\n        if the formset didn't validate.\n        "
    blank_formset = self.make_choiceformset([('', '')])
    self.assertFalse(blank_formset.has_changed())
    invalid_formset = self.make_choiceformset([('Calexico', '')])
    self.assertFalse(invalid_formset.is_valid())
    self.assertTrue(invalid_formset.has_changed())
    valid_formset = self.make_choiceformset([('Calexico', '100')])
    self.assertTrue(valid_formset.is_valid())
    self.assertTrue(valid_formset.has_changed())
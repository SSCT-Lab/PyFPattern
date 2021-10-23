def test_second_form_partially_filled(self):
    '\n        If at least one field is filled out on a blank form, it will be\n        validated.\n        '
    formset = self.make_choiceformset([('Calexico', '100'), ('The Decemberists', '')], initial_forms=1)
    self.assertFalse(formset.is_valid())
    self.assertEqual(formset.errors, [{
        
    }, {
        'votes': ['This field is required.'],
    }])
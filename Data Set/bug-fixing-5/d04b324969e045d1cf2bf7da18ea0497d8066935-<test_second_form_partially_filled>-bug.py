def test_second_form_partially_filled(self):
    formset = self.make_choiceformset([('Calexico', '100'), ('The Decemberists', '')], initial_forms=1)
    self.assertFalse(formset.is_valid())
    self.assertEqual(formset.errors, [{
        
    }, {
        'votes': ['This field is required.'],
    }])
def test_delete_prefilled_data(self):
    formset = self.make_choiceformset([('', ''), ('', '')], initial_forms=1)
    self.assertFalse(formset.is_valid())
    self.assertEqual(formset.errors, [{
        'votes': ['This field is required.'],
        'choice': ['This field is required.'],
    }, {
        
    }])
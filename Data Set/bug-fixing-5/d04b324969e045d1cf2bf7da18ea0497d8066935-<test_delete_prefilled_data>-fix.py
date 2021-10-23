def test_delete_prefilled_data(self):
    "\n        Deleting prefilled data is an error. Removing data from form fields\n        isn't the proper way to delete it.\n        "
    formset = self.make_choiceformset([('', ''), ('', '')], initial_forms=1)
    self.assertFalse(formset.is_valid())
    self.assertEqual(formset.errors, [{
        'votes': ['This field is required.'],
        'choice': ['This field is required.'],
    }, {
        
    }])
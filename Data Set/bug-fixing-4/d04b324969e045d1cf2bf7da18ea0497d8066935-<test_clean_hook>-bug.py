def test_clean_hook(self):
    data = {
        'drinks-TOTAL_FORMS': '2',
        'drinks-INITIAL_FORMS': '0',
        'drinks-MIN_NUM_FORMS': '0',
        'drinks-MAX_NUM_FORMS': '0',
        'drinks-0-name': 'Gin and Tonic',
        'drinks-1-name': 'Gin and Tonic',
    }
    formset = FavoriteDrinksFormSet(data, prefix='drinks')
    self.assertFalse(formset.is_valid())
    for error in formset.non_form_errors():
        self.assertEqual(str(error), 'You may only specify a drink once.')
    data = {
        'drinks-TOTAL_FORMS': '2',
        'drinks-INITIAL_FORMS': '0',
        'drinks-MIN_NUM_FORMS': '0',
        'drinks-MAX_NUM_FORMS': '0',
        'drinks-0-name': 'Gin and Tonic',
        'drinks-1-name': 'Bloody Mary',
    }
    formset = FavoriteDrinksFormSet(data, prefix='drinks')
    self.assertTrue(formset.is_valid())
    self.assertEqual(formset.non_form_errors(), [])
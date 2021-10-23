def test_empty_formset_is_valid(self):
    'An empty formset still calls clean()'
    EmptyFsetWontValidateFormset = formset_factory(FavoriteDrinkForm, extra=0, formset=EmptyFsetWontValidate)
    formset = EmptyFsetWontValidateFormset(data={
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '0',
    }, prefix='form')
    formset2 = EmptyFsetWontValidateFormset(data={
        'form-INITIAL_FORMS': '0',
        'form-TOTAL_FORMS': '1',
        'form-0-name': 'bah',
    }, prefix='form')
    self.assertFalse(formset.is_valid())
    self.assertFalse(formset2.is_valid())
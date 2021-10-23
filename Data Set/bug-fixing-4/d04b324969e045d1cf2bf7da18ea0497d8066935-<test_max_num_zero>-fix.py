def test_max_num_zero(self):
    '\n        If max_num is 0 then no form is rendered at all, regardless of extra,\n        unless initial data is present.\n        '
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=1, max_num=0)
    formset = LimitedFavoriteDrinkFormSet()
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertEqual('\n'.join(form_output), '')
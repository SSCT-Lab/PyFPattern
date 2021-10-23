def test_limiting_max_forms(self):
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=3)
    formset = LimitedFavoriteDrinkFormSet()
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertHTMLEqual('\n'.join(form_output), '<tr><th><label for="id_form-0-name">Name:</label></th>\n<td><input type="text" name="form-0-name" id="id_form-0-name" /></td></tr>\n<tr><th><label for="id_form-1-name">Name:</label></th>\n<td><input type="text" name="form-1-name" id="id_form-1-name" /></td></tr>\n<tr><th><label for="id_form-2-name">Name:</label></th>\n<td><input type="text" name="form-2-name" id="id_form-2-name" /></td></tr>')
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=3, max_num=0)
    formset = LimitedFavoriteDrinkFormSet()
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertEqual('\n'.join(form_output), '')
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=5, max_num=2)
    formset = LimitedFavoriteDrinkFormSet()
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertHTMLEqual('\n'.join(form_output), '<tr><th><label for="id_form-0-name">Name:</label></th><td>\n<input type="text" name="form-0-name" id="id_form-0-name" /></td></tr>\n<tr><th><label for="id_form-1-name">Name:</label></th>\n<td><input type="text" name="form-1-name" id="id_form-1-name" /></td></tr>')
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=1, max_num=2)
    formset = LimitedFavoriteDrinkFormSet()
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertHTMLEqual('\n'.join(form_output), '<tr><th><label for="id_form-0-name">Name:</label></th>\n<td><input type="text" name="form-0-name" id="id_form-0-name" /></td></tr>')
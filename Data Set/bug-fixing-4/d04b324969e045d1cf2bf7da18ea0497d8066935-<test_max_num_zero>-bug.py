def test_max_num_zero(self):
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=1, max_num=0)
    formset = LimitedFavoriteDrinkFormSet()
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertEqual('\n'.join(form_output), '')
    initial = [{
        'name': 'Fernet and Coke',
    }, {
        'name': 'Bloody Mary',
    }]
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=1, max_num=0)
    formset = LimitedFavoriteDrinkFormSet(initial=initial)
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertHTMLEqual('\n'.join(form_output), '<tr><th><label for="id_form-0-name">Name:</label></th>\n<td><input id="id_form-0-name" name="form-0-name" type="text" value="Fernet and Coke" /></td></tr>\n<tr><th><label for="id_form-1-name">Name:</label></th>\n<td><input id="id_form-1-name" name="form-1-name" type="text" value="Bloody Mary" /></td></tr>')
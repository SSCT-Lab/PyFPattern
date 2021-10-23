def test_max_num_with_initial_data(self):
    initial = [{
        'name': 'Fernet and Coke',
    }]
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=1)
    formset = LimitedFavoriteDrinkFormSet(initial=initial)
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertHTMLEqual('\n'.join(form_output), '<tr><th><label for="id_form-0-name">Name:</label></th>\n<td><input type="text" name="form-0-name" value="Fernet and Coke" id="id_form-0-name" /></td></tr>\n<tr><th><label for="id_form-1-name">Name:</label></th>\n<td><input type="text" name="form-1-name" id="id_form-1-name" /></td></tr>')
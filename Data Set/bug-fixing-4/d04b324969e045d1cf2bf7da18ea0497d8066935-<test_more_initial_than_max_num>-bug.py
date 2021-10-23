def test_more_initial_than_max_num(self):
    initial = [{
        'name': 'Gin Tonic',
    }, {
        'name': 'Bloody Mary',
    }, {
        'name': 'Jack and Coke',
    }]
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=1, max_num=2)
    formset = LimitedFavoriteDrinkFormSet(initial=initial)
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertHTMLEqual('\n'.join(form_output), '<tr><th><label for="id_form-0-name">Name:</label></th>\n<td><input id="id_form-0-name" name="form-0-name" type="text" value="Gin Tonic" /></td></tr>\n<tr><th><label for="id_form-1-name">Name:</label></th>\n<td><input id="id_form-1-name" name="form-1-name" type="text" value="Bloody Mary" /></td></tr>\n<tr><th><label for="id_form-2-name">Name:</label></th>\n<td><input id="id_form-2-name" name="form-2-name" type="text" value="Jack and Coke" /></td></tr>')
    initial = [{
        'name': 'Gin Tonic',
    }]
    LimitedFavoriteDrinkFormSet = formset_factory(FavoriteDrinkForm, extra=3, max_num=2)
    formset = LimitedFavoriteDrinkFormSet(initial=initial)
    form_output = []
    for form in formset.forms:
        form_output.append(str(form))
    self.assertHTMLEqual('\n'.join(form_output), '<tr><th><label for="id_form-0-name">Name:</label></th>\n<td><input type="text" name="form-0-name" value="Gin Tonic" id="id_form-0-name" /></td></tr>\n<tr><th><label for="id_form-1-name">Name:</label></th>\n<td><input type="text" name="form-1-name" id="id_form-1-name" /></td></tr>')
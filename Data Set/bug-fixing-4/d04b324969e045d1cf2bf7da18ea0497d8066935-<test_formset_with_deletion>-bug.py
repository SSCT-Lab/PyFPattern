def test_formset_with_deletion(self):
    ChoiceFormSet = formset_factory(Choice, can_delete=True)
    initial = [{
        'choice': 'Calexico',
        'votes': 100,
    }, {
        'choice': 'Fergie',
        'votes': 900,
    }]
    formset = ChoiceFormSet(initial=initial, auto_id=False, prefix='choices')
    form_output = []
    for form in formset.forms:
        form_output.append(form.as_ul())
    self.assertHTMLEqual('\n'.join(form_output), '<li>Choice: <input type="text" name="choices-0-choice" value="Calexico" /></li>\n<li>Votes: <input type="number" name="choices-0-votes" value="100" /></li>\n<li>Delete: <input type="checkbox" name="choices-0-DELETE" /></li>\n<li>Choice: <input type="text" name="choices-1-choice" value="Fergie" /></li>\n<li>Votes: <input type="number" name="choices-1-votes" value="900" /></li>\n<li>Delete: <input type="checkbox" name="choices-1-DELETE" /></li>\n<li>Choice: <input type="text" name="choices-2-choice" /></li>\n<li>Votes: <input type="number" name="choices-2-votes" /></li>\n<li>Delete: <input type="checkbox" name="choices-2-DELETE" /></li>')
    data = {
        'choices-TOTAL_FORMS': '3',
        'choices-INITIAL_FORMS': '2',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
        'choices-0-choice': 'Calexico',
        'choices-0-votes': '100',
        'choices-0-DELETE': '',
        'choices-1-choice': 'Fergie',
        'choices-1-votes': '900',
        'choices-1-DELETE': 'on',
        'choices-2-choice': '',
        'choices-2-votes': '',
        'choices-2-DELETE': '',
    }
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertTrue(formset.is_valid())
    self.assertEqual([form.cleaned_data for form in formset.forms], [{
        'votes': 100,
        'DELETE': False,
        'choice': 'Calexico',
    }, {
        'votes': 900,
        'DELETE': True,
        'choice': 'Fergie',
    }, {
        
    }])
    self.assertEqual([form.cleaned_data for form in formset.deleted_forms], [{
        'votes': 900,
        'DELETE': True,
        'choice': 'Fergie',
    }])

    class CheckForm(Form):
        field = IntegerField(min_value=100)
    data = {
        'check-TOTAL_FORMS': '3',
        'check-INITIAL_FORMS': '2',
        'choices-MIN_NUM_FORMS': '0',
        'check-MAX_NUM_FORMS': '0',
        'check-0-field': '200',
        'check-0-DELETE': '',
        'check-1-field': '50',
        'check-1-DELETE': 'on',
        'check-2-field': '',
        'check-2-DELETE': '',
    }
    CheckFormSet = formset_factory(CheckForm, can_delete=True)
    formset = CheckFormSet(data, prefix='check')
    self.assertTrue(formset.is_valid())
    data['check-1-DELETE'] = ''
    formset = CheckFormSet(data, prefix='check')
    self.assertFalse(formset.is_valid())

    class Person(Form):
        name = CharField()
    PeopleForm = formset_factory(form=Person, can_delete=True)
    p = PeopleForm({
        'form-0-name': '',
        'form-0-DELETE': 'on',
        'form-TOTAL_FORMS': 1,
        'form-INITIAL_FORMS': 1,
        'form-MIN_NUM_FORMS': 0,
        'form-MAX_NUM_FORMS': 1,
    })
    self.assertTrue(p.is_valid())
    self.assertEqual(p._errors, [])
    self.assertEqual(len(p.deleted_forms), 1)
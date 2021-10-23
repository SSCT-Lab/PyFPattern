def test_formset_calls_forms_is_valid(self):
    'Formsets call is_valid() on each form.'

    class AnotherChoice(Choice):

        def is_valid(self):
            self.is_valid_called = True
            return super().is_valid()
    AnotherChoiceFormSet = formset_factory(AnotherChoice)
    data = {
        'choices-TOTAL_FORMS': '1',
        'choices-INITIAL_FORMS': '0',
        'choices-MIN_NUM_FORMS': '0',
        'choices-MAX_NUM_FORMS': '0',
        'choices-0-choice': 'Calexico',
        'choices-0-votes': '100',
    }
    formset = AnotherChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertTrue(formset.is_valid())
    self.assertTrue(all((form.is_valid_called for form in formset.forms)))
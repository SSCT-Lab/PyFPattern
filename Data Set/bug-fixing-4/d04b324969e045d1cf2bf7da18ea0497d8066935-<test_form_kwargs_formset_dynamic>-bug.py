def test_form_kwargs_formset_dynamic(self):
    '\n        Form kwargs can be passed dynamically in a formset.\n        '

    class DynamicBaseFormSet(BaseFormSet):

        def get_form_kwargs(self, index):
            return {
                'custom_kwarg': index,
            }
    DynamicFormSet = formset_factory(CustomKwargForm, formset=DynamicBaseFormSet, extra=2)
    formset = DynamicFormSet(form_kwargs={
        'custom_kwarg': 'ignored',
    })
    for (i, form) in enumerate(formset):
        self.assertTrue(hasattr(form, 'custom_kwarg'))
        self.assertEqual(form.custom_kwarg, i)
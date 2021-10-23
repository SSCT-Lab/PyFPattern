def test_non_form_errors_run_full_clean(self):
    '\n        If non_form_errors() is called without calling is_valid() first,\n        it should ensure that full_clean() is called.\n        '

    class BaseCustomFormSet(BaseFormSet):

        def clean(self):
            raise ValidationError('This is a non-form error')
    ChoiceFormSet = formset_factory(Choice, formset=BaseCustomFormSet)
    formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
    self.assertIsInstance(formset.non_form_errors(), ErrorList)
    self.assertEqual(list(formset.non_form_errors()), ['This is a non-form error'])
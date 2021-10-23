def test_formset_error_class(self):
    "Formset's forms use the formset's error_class."

    class CustomErrorList(ErrorList):
        pass
    formset = FavoriteDrinksFormSet(error_class=CustomErrorList)
    self.assertEqual(formset.forms[0].error_class, CustomErrorList)
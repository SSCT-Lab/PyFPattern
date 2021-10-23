def test_formset_error_class(self):

    class CustomErrorList(ErrorList):
        pass
    formset = FavoriteDrinksFormSet(error_class=CustomErrorList)
    self.assertEqual(formset.forms[0].error_class, CustomErrorList)
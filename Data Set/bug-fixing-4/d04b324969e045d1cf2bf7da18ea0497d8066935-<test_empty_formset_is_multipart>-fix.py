def test_empty_formset_is_multipart(self):
    'is_multipart() works with an empty formset.'

    class FileForm(Form):
        file = FileField()
    self.assertTrue(formset_factory(FileForm, extra=0)().is_multipart())
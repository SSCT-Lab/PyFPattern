def test_empty_formset_is_multipart(self):
    'Make sure `is_multipart()` works with empty formset, refs #19545'

    class FileForm(Form):
        file = FileField()
    self.assertTrue(formset_factory(FileForm, extra=0)().is_multipart())
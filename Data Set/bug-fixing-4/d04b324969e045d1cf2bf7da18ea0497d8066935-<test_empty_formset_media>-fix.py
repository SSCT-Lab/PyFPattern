def test_empty_formset_media(self):
    'Media is available on empty formset.'

    class MediaForm(Form):

        class Media():
            js = ('some-file.js',)
    self.assertIn('some-file.js', str(formset_factory(MediaForm, extra=0)().media))
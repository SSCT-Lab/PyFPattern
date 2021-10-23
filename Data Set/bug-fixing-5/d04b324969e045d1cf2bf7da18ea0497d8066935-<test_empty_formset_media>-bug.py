def test_empty_formset_media(self):
    'Make sure media is available on empty formset, refs #19545'

    class MediaForm(Form):

        class Media():
            js = ('some-file.js',)
    self.assertIn('some-file.js', str(formset_factory(MediaForm, extra=0)().media))
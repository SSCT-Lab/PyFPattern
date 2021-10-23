def test_count_does_not_silence_attribute_error(self):

    class AttributeErrorContainer():

        def count(self):
            raise AttributeError('abc')
    with self.assertRaisesMessage(AttributeError, 'abc'):
        Paginator(AttributeErrorContainer(), 10).count
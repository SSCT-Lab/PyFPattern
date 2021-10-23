def test_count_does_not_silence_type_error(self):

    class TypeErrorContainer():

        def count(self):
            raise TypeError('abc')
    with self.assertRaisesMessage(TypeError, 'abc'):
        Paginator(TypeErrorContainer(), 10).count
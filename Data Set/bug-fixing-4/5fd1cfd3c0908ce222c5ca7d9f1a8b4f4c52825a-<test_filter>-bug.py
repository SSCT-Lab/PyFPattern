def test_filter(self):
    (filters, query) = separate_filters_from_query('author:foo')
    self.assertDictEqual(filters, {
        'author': 'foo',
    })
    self.assertEquals(query, '')
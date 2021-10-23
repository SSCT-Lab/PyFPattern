def test_filter_and_query(self):
    (filters, query) = separate_filters_from_query('author:foo hello world')
    self.assertDictEqual(filters, {
        'author': 'foo',
    })
    self.assertEqual(query, 'hello world')
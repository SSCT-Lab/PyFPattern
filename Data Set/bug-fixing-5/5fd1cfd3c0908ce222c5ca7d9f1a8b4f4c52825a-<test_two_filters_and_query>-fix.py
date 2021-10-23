def test_two_filters_and_query(self):
    (filters, query) = separate_filters_from_query('author:"foo bar" hello world bar:beer')
    self.assertDictEqual(filters, {
        'author': 'foo bar',
        'bar': 'beer',
    })
    self.assertEqual(query, 'hello world')
def test_filter_with_quotation_mark_and_query(self):
    (filters, query) = separate_filters_from_query('author:"foo bar" hello world')
    self.assertDictEqual(filters, {
        'author': 'foo bar',
    })
    self.assertEquals(query, 'hello world')
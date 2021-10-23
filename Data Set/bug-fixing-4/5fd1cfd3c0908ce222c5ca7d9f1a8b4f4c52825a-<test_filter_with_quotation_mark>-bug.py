def test_filter_with_quotation_mark(self):
    (filters, query) = separate_filters_from_query('author:"foo bar"')
    self.assertDictEqual(filters, {
        'author': 'foo bar',
    })
    self.assertEquals(query, '')
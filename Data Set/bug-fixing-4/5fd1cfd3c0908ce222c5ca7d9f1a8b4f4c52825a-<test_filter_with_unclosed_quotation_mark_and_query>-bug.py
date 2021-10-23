def test_filter_with_unclosed_quotation_mark_and_query(self):
    (filters, query) = separate_filters_from_query('author:"foo bar hello world')
    self.assertDictEqual(filters, {
        
    })
    self.assertEquals(query, 'author:"foo bar hello world')
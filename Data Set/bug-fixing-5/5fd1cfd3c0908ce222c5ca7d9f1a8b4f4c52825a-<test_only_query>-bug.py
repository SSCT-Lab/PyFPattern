def test_only_query(self):
    (filters, query) = separate_filters_from_query('hello world')
    self.assertDictEqual(filters, {
        
    })
    self.assertEquals(query, 'hello world')
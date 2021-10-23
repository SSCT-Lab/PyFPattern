def test_constructor_manager_resize(self):
    index = list(self.frame.index[:5])
    columns = list(self.frame.columns[:3])
    result = DataFrame(self.frame._data, index=index, columns=columns)
    tm.assert_index_equal(result.index, Index(index))
    tm.assert_index_equal(result.columns, Index(columns))
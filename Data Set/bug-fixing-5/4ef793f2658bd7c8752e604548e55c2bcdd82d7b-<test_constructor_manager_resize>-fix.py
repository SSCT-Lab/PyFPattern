def test_constructor_manager_resize(self, float_frame):
    index = list(float_frame.index[:5])
    columns = list(float_frame.columns[:3])
    result = DataFrame(float_frame._data, index=index, columns=columns)
    tm.assert_index_equal(result.index, Index(index))
    tm.assert_index_equal(result.columns, Index(columns))
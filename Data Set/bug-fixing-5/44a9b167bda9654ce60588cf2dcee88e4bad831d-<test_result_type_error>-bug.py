@pytest.mark.parametrize('result_type', ['foo', 1])
def test_result_type_error(self, result_type):
    df = DataFrame((np.tile(np.arange(3, dtype='int64'), 6).reshape(6, (- 1)) + 1), columns=['A', 'B', 'C'])
    with pytest.raises(ValueError):
        df.apply((lambda x: [1, 2, 3]), axis=1, result_type=result_type)
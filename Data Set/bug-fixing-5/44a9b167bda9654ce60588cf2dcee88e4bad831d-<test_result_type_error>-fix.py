@pytest.mark.parametrize('result_type', ['foo', 1])
def test_result_type_error(self, result_type, int_frame_const_col):
    df = int_frame_const_col
    with pytest.raises(ValueError):
        df.apply((lambda x: [1, 2, 3]), axis=1, result_type=result_type)
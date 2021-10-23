def test_fillna_invalid_method(self, float_frame):
    with pytest.raises(ValueError, match='ffil'):
        float_frame.fillna(method='ffil')
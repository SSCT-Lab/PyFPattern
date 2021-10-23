def test_fillna_invalid_value(self, float_frame):
    msg = '"value" parameter must be a scalar or dict, but you passed a "{}"'
    with pytest.raises(TypeError, match=msg.format('list')):
        float_frame.fillna([1, 2])
    with pytest.raises(TypeError, match=msg.format('tuple')):
        float_frame.fillna((1, 2))
    msg = '"value" parameter must be a scalar, dict or Series, but you passed a "DataFrame"'
    with pytest.raises(TypeError, match=msg):
        float_frame.iloc[:, 0].fillna(float_frame)
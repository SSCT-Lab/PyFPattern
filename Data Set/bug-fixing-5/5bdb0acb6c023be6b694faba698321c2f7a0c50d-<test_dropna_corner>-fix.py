def test_dropna_corner(self, float_frame):
    msg = 'invalid how option: foo'
    with pytest.raises(ValueError, match=msg):
        float_frame.dropna(how='foo')
    msg = 'must specify how or thresh'
    with pytest.raises(TypeError, match=msg):
        float_frame.dropna(how=None)
    with pytest.raises(KeyError, match="^\\['X'\\]$"):
        float_frame.dropna(subset=['A', 'X'])
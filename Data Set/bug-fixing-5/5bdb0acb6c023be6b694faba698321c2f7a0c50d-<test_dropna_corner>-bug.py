def test_dropna_corner(self):
    msg = 'invalid how option: foo'
    with pytest.raises(ValueError, match=msg):
        self.frame.dropna(how='foo')
    msg = 'must specify how or thresh'
    with pytest.raises(TypeError, match=msg):
        self.frame.dropna(how=None)
    with pytest.raises(KeyError, match="^\\['X'\\]$"):
        self.frame.dropna(subset=['A', 'X'])
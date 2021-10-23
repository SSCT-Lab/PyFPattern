def test_fillna_invalid_method(self):
    with pytest.raises(ValueError, match='ffil'):
        self.frame.fillna(method='ffil')
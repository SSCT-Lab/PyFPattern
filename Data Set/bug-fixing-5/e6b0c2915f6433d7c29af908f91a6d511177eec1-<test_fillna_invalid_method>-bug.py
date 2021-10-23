def test_fillna_invalid_method(self):
    try:
        self.ts.fillna(method='ffil')
    except ValueError as inst:
        assert ('ffil' in str(inst))
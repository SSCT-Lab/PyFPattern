def test_transform_and_agg_error(self):

    def f():
        self.series.transform(['min', 'max'])
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            self.series.agg(['sqrt', 'max'])
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            self.series.transform(['sqrt', 'max'])
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            self.series.agg({
                'foo': np.sqrt,
                'bar': 'sum',
            })
    pytest.raises(ValueError, f)
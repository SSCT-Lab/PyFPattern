def test_transform_and_agg_err(self, axis):

    def f():
        self.frame.transform(['max', 'min'], axis=axis)
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            self.frame.agg(['max', 'sqrt'], axis=axis)
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            self.frame.transform(['max', 'sqrt'], axis=axis)
    pytest.raises(ValueError, f)
    df = pd.DataFrame({
        'A': range(5),
        'B': 5,
    })

    def f():
        with np.errstate(all='ignore'):
            df.agg({
                'A': ['abs', 'sum'],
                'B': ['mean', 'max'],
            }, axis=axis)
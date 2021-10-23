def test_transform_and_agg_err(self, axis, float_frame):

    def f():
        float_frame.transform(['max', 'min'], axis=axis)
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            float_frame.agg(['max', 'sqrt'], axis=axis)
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            float_frame.transform(['max', 'sqrt'], axis=axis)
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
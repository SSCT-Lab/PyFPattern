def test_with_string_args(self):
    for arg in ['sum', 'mean', 'min', 'max', 'std']:
        result = self.ts.apply(arg)
        expected = getattr(self.ts, arg)()
        assert (result == expected)
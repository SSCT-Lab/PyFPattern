def test_agg_transform(self, axis):
    other_axis = (1 if (axis in {0, 'index'}) else 0)
    with np.errstate(all='ignore'):
        f_abs = np.abs(self.frame)
        f_sqrt = np.sqrt(self.frame)
        result = self.frame.transform(np.sqrt, axis=axis)
        expected = f_sqrt.copy()
        assert_frame_equal(result, expected)
        result = self.frame.apply(np.sqrt, axis=axis)
        assert_frame_equal(result, expected)
        result = self.frame.transform(np.sqrt, axis=axis)
        assert_frame_equal(result, expected)
        result = self.frame.apply([np.sqrt], axis=axis)
        expected = f_sqrt.copy()
        if (axis in {0, 'index'}):
            expected.columns = pd.MultiIndex.from_product([self.frame.columns, ['sqrt']])
        else:
            expected.index = pd.MultiIndex.from_product([self.frame.index, ['sqrt']])
        assert_frame_equal(result, expected)
        result = self.frame.transform([np.sqrt], axis=axis)
        assert_frame_equal(result, expected)
        result = self.frame.apply([np.abs, np.sqrt], axis=axis)
        expected = zip_frames([f_abs, f_sqrt], axis=other_axis)
        if (axis in {0, 'index'}):
            expected.columns = pd.MultiIndex.from_product([self.frame.columns, ['absolute', 'sqrt']])
        else:
            expected.index = pd.MultiIndex.from_product([self.frame.index, ['absolute', 'sqrt']])
        assert_frame_equal(result, expected)
        result = self.frame.transform([np.abs, 'sqrt'], axis=axis)
        assert_frame_equal(result, expected)
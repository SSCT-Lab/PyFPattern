def test_transform_array(self):
    names = self.data.index.names
    transformed_array = self.grouping.transform_array(self.data.values, (lambda x: x.mean()), level=0)
    grouped = self.data.reset_index().groupby(names[0])
    expected = grouped.apply((lambda x: x.mean()))[self.data.columns]
    np.testing.assert_allclose(transformed_array, expected.values)
    if (len(names) > 1):
        transformed_array = self.grouping.transform_array(self.data.values, (lambda x: x.mean()), level=1)
        grouped = self.data.reset_index().groupby(names[1])
        expected = grouped.apply((lambda x: x.mean()))[self.data.columns]
        np.testing.assert_allclose(transformed_array, expected.values)
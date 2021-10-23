def test_transform_dataframe(self):
    names = self.data.index.names
    transformed_dataframe = self.grouping.transform_dataframe(self.data, (lambda x: x.mean()), level=0)
    grouped = self.data.reset_index().groupby(names[0])
    expected = grouped.apply((lambda x: x.mean()))[self.data.columns]
    np.testing.assert_allclose(transformed_dataframe, expected.values)
    if (len(names) > 1):
        transformed_dataframe = self.grouping.transform_dataframe(self.data, (lambda x: x.mean()), level=1)
        grouped = self.data.reset_index().groupby(names[1])
        expected = grouped.apply((lambda x: x.mean()))[self.data.columns]
        np.testing.assert_allclose(transformed_dataframe, expected.values)
def test_append(self):
    appendedSeries = self.series.append(self.objSeries)
    for (idx, value) in compat.iteritems(appendedSeries):
        if (idx in self.series.index):
            assert (value == self.series[idx])
        elif (idx in self.objSeries.index):
            assert (value == self.objSeries[idx])
        else:
            raise AssertionError('orphaned index!')
    pytest.raises(ValueError, self.ts.append, self.ts, verify_integrity=True)
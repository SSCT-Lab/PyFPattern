

def test_bins_not_overlapping_from_intervalindex(self):
    ii = IntervalIndex.from_tuples([(0, 10), (2, 12), (4, 14)])
    with pytest.raises(ValueError):
        cut([5, 6], bins=ii)

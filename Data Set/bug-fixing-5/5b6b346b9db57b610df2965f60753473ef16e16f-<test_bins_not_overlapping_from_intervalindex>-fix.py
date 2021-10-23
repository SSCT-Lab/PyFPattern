def test_bins_not_overlapping_from_intervalindex(self):
    msg = 'Overlapping IntervalIndex is not accepted'
    ii = IntervalIndex.from_tuples([(0, 10), (2, 12), (4, 14)])
    with pytest.raises(ValueError, match=msg):
        cut([5, 6], bins=ii)
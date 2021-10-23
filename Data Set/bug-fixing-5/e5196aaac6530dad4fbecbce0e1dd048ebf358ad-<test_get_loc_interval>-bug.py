@pytest.mark.parametrize('idx_side', ['right', 'left', 'both', 'neither'])
@pytest.mark.parametrize('side', ['right', 'left', 'both', 'neither'])
def test_get_loc_interval(self, idx_side, side):
    idx = IntervalIndex.from_tuples([(0, 1), (2, 3)], closed=idx_side)
    for bound in [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [2.5, 3], [(- 1), 4]]:
        if (idx_side == side):
            if (bound == [0, 1]):
                assert (idx.get_loc(Interval(0, 1, closed=side)) == 0)
            elif (bound == [2, 3]):
                assert (idx.get_loc(Interval(2, 3, closed=side)) == 1)
            else:
                with pytest.raises(KeyError):
                    idx.get_loc(Interval(*bound, closed=side))
        else:
            with pytest.raises(KeyError):
                idx.get_loc(Interval(*bound, closed=side))
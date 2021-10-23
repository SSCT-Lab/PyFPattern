@pytest.mark.parametrize('idx_side', ['right', 'left', 'both', 'neither'])
@pytest.mark.parametrize('scalar', [(- 0.5), 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5])
def test_get_loc_scalar(self, idx_side, scalar):
    correct = {
        'right': {
            0.5: 0,
            1: 0,
            2.5: 1,
            3: 1,
        },
        'left': {
            0: 0,
            0.5: 0,
            2: 1,
            2.5: 1,
        },
        'both': {
            0: 0,
            0.5: 0,
            1: 0,
            2: 1,
            2.5: 1,
            3: 1,
        },
        'neither': {
            0.5: 0,
            2.5: 1,
        },
    }
    idx = IntervalIndex.from_tuples([(0, 1), (2, 3)], closed=idx_side)
    if (scalar in correct[idx_side].keys()):
        assert (idx.get_loc(scalar) == correct[idx_side][scalar])
    else:
        pytest.raises(KeyError, idx.get_loc, scalar)
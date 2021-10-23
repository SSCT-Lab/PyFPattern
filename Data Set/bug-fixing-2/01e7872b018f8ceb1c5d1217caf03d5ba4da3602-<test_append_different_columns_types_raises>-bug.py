

@pytest.mark.parametrize('index_can_append', indexes_can_append, ids=(lambda x: x.__class__.__name__))
@pytest.mark.parametrize('index_cannot_append_with_other', indexes_cannot_append_with_other, ids=(lambda x: x.__class__.__name__))
def test_append_different_columns_types_raises(self, index_can_append, index_cannot_append_with_other):
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=index_can_append)
    ser = pd.Series([7, 8, 9], index=index_cannot_append_with_other, name=2)
    msg = "the other index needs to be an IntervalIndex too, but was type {}|object of type '(int|long|float|Timestamp)' has no len\\(\\)|Expected tuple, got str"
    with pytest.raises(TypeError, match=msg.format(index_can_append.__class__.__name__)):
        df.append(ser)
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=index_cannot_append_with_other)
    ser = pd.Series([7, 8, 9], index=index_can_append, name=2)
    msg = "unorderable types: (Interval|int)\\(\\) > (int|long|float|str)\\(\\)|Expected tuple, got (int|long|float|str)|Cannot compare type 'Timestamp' with type '(int|long)'"
    with pytest.raises(TypeError, match=msg):
        df.append(ser)

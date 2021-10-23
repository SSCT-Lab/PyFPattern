@given(index=indices(max_length=5), num_columns=integers(0, 5))
@settings(deadline=1000)
def test_frequency_is_original(self, index, num_columns):
    original = index.copy()
    df = DataFrame(True, index=index, columns=range(num_columns))
    df.apply((lambda x: x))
    assert (index.freq == original.freq)
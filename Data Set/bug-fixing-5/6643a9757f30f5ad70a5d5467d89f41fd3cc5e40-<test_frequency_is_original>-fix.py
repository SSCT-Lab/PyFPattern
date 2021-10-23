@pytest.mark.parametrize('num_cols', [2, 3, 5])
def test_frequency_is_original(self, num_cols):
    index = pd.DatetimeIndex(['1950-06-30', '1952-10-24', '1953-05-29'])
    original = index.copy()
    df = DataFrame(1, index=index, columns=range(num_cols))
    df.apply((lambda x: x))
    assert (index.freq == original.freq)
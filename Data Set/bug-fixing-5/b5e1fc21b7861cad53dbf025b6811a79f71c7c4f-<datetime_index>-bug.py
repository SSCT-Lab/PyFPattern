@pytest.fixture(params=['D', 'B', 'W', 'M', 'Q', 'Y'])
def datetime_index(request):
    '\n    A fixture to provide DatetimeIndex objects with different frequencies.\n\n    Most DatetimeArray behavior is already tested in DatetimeIndex tests,\n    so here we just test that the DatetimeIndex behavior matches\n    the DatetimeIndex behavior.\n    '
    freqstr = request.param
    pi = pd.date_range(start=pd.Timestamp('2000-01-01'), periods=100, freq=freqstr)
    return pi
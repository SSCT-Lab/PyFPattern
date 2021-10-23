@pytest.fixture
def timezone_frame():
    "\n    Fixture for DataFrame of date_range Series with different time zones\n\n    Columns are ['A', 'B', 'C']; some entries are missing\n    "
    df = DataFrame({
        'A': date_range('20130101', periods=3),
        'B': date_range('20130101', periods=3, tz='US/Eastern'),
        'C': date_range('20130101', periods=3, tz='CET'),
    })
    df.iloc[(1, 1)] = NaT
    df.iloc[(1, 2)] = NaT
    return df
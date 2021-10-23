@pytest.fixture
def bool_frame_with_na():
    "\n    Fixture for DataFrame of booleans with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D']; some entries are missing\n\n                    A      B      C      D\n    zBZxY2IDGd  False  False  False  False\n    IhBWBMWllt  False   True   True   True\n    ctjdvZSR6R   True  False   True   True\n    AVTujptmxb  False   True  False   True\n    G9lrImrSWq  False  False  False   True\n    sFFwdIUfz2    NaN    NaN    NaN    NaN\n    s15ptEJnRb    NaN    NaN    NaN    NaN\n    ...           ...    ...    ...    ...\n    UW41KkDyZ4   True   True  False  False\n    l9l6XkOdqV   True  False  False  False\n    X2MeZfzDYA  False   True  False  False\n    xWkIKU7vfX  False   True  False   True\n    QOhL6VmpGU  False  False  False   True\n    22PwkRJdat  False   True  False  False\n    kfboQ3VeIK   True  False   True  False\n\n    [30 rows x 4 columns]\n    "
    df = (DataFrame(tm.getSeriesData()) > 0)
    df = df.astype(object)
    df.loc[5:10] = np.nan
    df.loc[15:20, (- 2):] = np.nan
    return df
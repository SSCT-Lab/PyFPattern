def get_expects(self):
    expects = {
        'sr1': {
            'count': Series([1, 2, 2, 2, 2], dtype='float64'),
            'max': Series([np.nan, 1, 2, 3, 4], dtype='float64'),
            'min': Series([np.nan, 0, 1, 2, 3], dtype='float64'),
            'sum': Series([np.nan, 1, 3, 5, 7], dtype='float64'),
            'mean': Series([np.nan, 0.5, 1.5, 2.5, 3.5], dtype='float64'),
            'std': Series(([np.nan] + ([np.sqrt(0.5)] * 4)), dtype='float64'),
            'var': Series([np.nan, 0.5, 0.5, 0.5, 0.5], dtype='float64'),
            'median': Series([np.nan, 0.5, 1.5, 2.5, 3.5], dtype='float64'),
        },
        'sr2': {
            'count': Series([1, 2, 2, 2, 2], dtype='float64'),
            'max': Series([np.nan, 10, 8, 6, 4], dtype='float64'),
            'min': Series([np.nan, 8, 6, 4, 2], dtype='float64'),
            'sum': Series([np.nan, 18, 14, 10, 6], dtype='float64'),
            'mean': Series([np.nan, 9, 7, 5, 3], dtype='float64'),
            'std': Series(([np.nan] + ([np.sqrt(2)] * 4)), dtype='float64'),
            'var': Series([np.nan, 2, 2, 2, 2], dtype='float64'),
            'median': Series([np.nan, 9, 7, 5, 3], dtype='float64'),
        },
        'sr3': {
            'count': Series([1, 2, 2, 1, 1], dtype='float64'),
            'max': Series([np.nan, 1, 2, np.nan, np.nan], dtype='float64'),
            'min': Series([np.nan, 0, 1, np.nan, np.nan], dtype='float64'),
            'sum': Series([np.nan, 1, 3, np.nan, np.nan], dtype='float64'),
            'mean': Series([np.nan, 0.5, 1.5, np.nan, np.nan], dtype='float64'),
            'std': Series((([np.nan] + ([np.sqrt(0.5)] * 2)) + ([np.nan] * 2)), dtype='float64'),
            'var': Series([np.nan, 0.5, 0.5, np.nan, np.nan], dtype='float64'),
            'median': Series([np.nan, 0.5, 1.5, np.nan, np.nan], dtype='float64'),
        },
        'df': {
            'count': DataFrame({
                0: Series([1, 2, 2, 2, 2]),
                1: Series([1, 2, 2, 2, 2]),
            }, dtype='float64'),
            'max': DataFrame({
                0: Series([np.nan, 2, 4, 6, 8]),
                1: Series([np.nan, 3, 5, 7, 9]),
            }, dtype='float64'),
            'min': DataFrame({
                0: Series([np.nan, 0, 2, 4, 6]),
                1: Series([np.nan, 1, 3, 5, 7]),
            }, dtype='float64'),
            'sum': DataFrame({
                0: Series([np.nan, 2, 6, 10, 14]),
                1: Series([np.nan, 4, 8, 12, 16]),
            }, dtype='float64'),
            'mean': DataFrame({
                0: Series([np.nan, 1, 3, 5, 7]),
                1: Series([np.nan, 2, 4, 6, 8]),
            }, dtype='float64'),
            'std': DataFrame({
                0: Series(([np.nan] + ([np.sqrt(2)] * 4))),
                1: Series(([np.nan] + ([np.sqrt(2)] * 4))),
            }, dtype='float64'),
            'var': DataFrame({
                0: Series([np.nan, 2, 2, 2, 2]),
                1: Series([np.nan, 2, 2, 2, 2]),
            }, dtype='float64'),
            'median': DataFrame({
                0: Series([np.nan, 1, 3, 5, 7]),
                1: Series([np.nan, 2, 4, 6, 8]),
            }, dtype='float64'),
        },
    }
    return expects
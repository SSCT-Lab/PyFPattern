def quotes_historical_google(symbol, date1, date2):
    'Get the historical data from Google finance.\n\n    Parameters\n    ----------\n    symbol : str\n        Ticker symbol to query for, for example ``"DELL"``.\n    date1 : datetime.datetime\n        Start date.\n    date2 : datetime.datetime\n        End date.\n\n    Returns\n    -------\n    X : array\n        The columns are ``date`` -- datetime, ``open``, ``high``,\n        ``low``, ``close`` and ``volume`` of type float.\n    '
    params = urlencode({
        'q': symbol,
        'startdate': date1.strftime('%b %d, %Y'),
        'enddate': date2.strftime('%b %d, %Y'),
        'output': 'csv',
    })
    url = ('http://www.google.com/finance/historical?' + params)
    with urlopen(url) as response:
        dtype = {
            'names': ['date', 'open', 'high', 'low', 'close', 'volume'],
            'formats': ['object', 'f4', 'f4', 'f4', 'f4', 'f4'],
        }
        converters = {
            0: (lambda s: datetime.strptime(s.decode(), '%d-%b-%y')),
        }
        return np.genfromtxt(response, delimiter=',', skip_header=1, dtype=dtype, converters=converters, missing_values='-', filling_values=(- 1))
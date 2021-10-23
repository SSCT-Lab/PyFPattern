def quotes_historical_google(symbol, start_date, end_date):
    'Get the historical data from Google finance.\n\n    Parameters\n    ----------\n    symbol : str\n        Ticker symbol to query for, for example ``"DELL"``.\n    start_date : datetime.datetime\n        Start date.\n    end_date : datetime.datetime\n        End date.\n\n    Returns\n    -------\n    X : array\n        The columns are ``date`` -- date, ``open``, ``high``,\n        ``low``, ``close`` and ``volume`` of type float.\n    '
    params = {
        'q': symbol,
        'startdate': start_date.strftime('%Y-%m-%d'),
        'enddate': end_date.strftime('%Y-%m-%d'),
        'output': 'csv',
    }
    url = ('https://finance.google.com/finance/historical?' + urlencode(params))
    response = urlopen(url)
    dtype = {
        'names': ['date', 'open', 'high', 'low', 'close', 'volume'],
        'formats': ['object', 'f4', 'f4', 'f4', 'f4', 'f4'],
    }
    converters = {
        0: (lambda s: datetime.strptime(s.decode(), '%d-%b-%y').date()),
    }
    data = np.genfromtxt(response, delimiter=',', skip_header=1, dtype=dtype, converters=converters, missing_values='-', filling_values=(- 1))
    min_date = (min(data['date']) if len(data) else datetime.min.date())
    max_date = (max(data['date']) if len(data) else datetime.max.date())
    start_end_diff = (end_date - start_date).days
    min_max_diff = (max_date - min_date).days
    data_is_fine = ((start_date <= min_date <= end_date) and (start_date <= max_date <= end_date) and ((start_end_diff - 7) <= min_max_diff <= start_end_diff))
    if (not data_is_fine):
        message = 'Data looks wrong for symbol {}, url {}\n  - start_date: {}, end_date: {}\n  - min_date:   {}, max_date: {}\n  - start_end_diff: {}, min_max_diff: {}'.format(symbol, url, start_date, end_date, min_date, max_date, start_end_diff, min_max_diff)
        raise RuntimeError(message)
    return data
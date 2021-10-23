

@tm.network
def test_pandas_datareader():
    pandas_datareader = import_module('pandas_datareader')
    pandas_datareader.DataReader('F', 'quandl', '2017-01-01', '2017-02-01')

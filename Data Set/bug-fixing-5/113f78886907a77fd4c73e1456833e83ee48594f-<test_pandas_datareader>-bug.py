@tm.network
def test_pandas_datareader():
    pandas_datareader = import_module('pandas_datareader')
    pandas_datareader.get_data_google('AAPL')
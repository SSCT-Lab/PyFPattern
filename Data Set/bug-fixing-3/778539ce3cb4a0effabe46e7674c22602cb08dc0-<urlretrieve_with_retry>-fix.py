@retry(initial_delay=1.0, max_delay=16.0, is_retriable=_is_retriable)
def urlretrieve_with_retry(url, filename=None):
    return urllib.request.urlretrieve(url, filename)
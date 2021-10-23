def try_repeated(func):
    'Runs a function a few times ignoring errors we see from GCS\n    due to what appears to be network issues.  This is a temporary workaround\n    until we can find the root cause.\n    '
    idx = 0
    while 1:
        try:
            return func()
        except (DataCorruption, ConnectionError, TransportError):
            if (idx >= 3):
                raise
        idx += 1
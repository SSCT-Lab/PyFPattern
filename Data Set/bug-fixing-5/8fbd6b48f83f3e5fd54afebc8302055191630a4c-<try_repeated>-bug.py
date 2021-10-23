def try_repeated(func):
    '\n    Runs a function a few times ignoring errors we see from GCS\n    due to what appears to be network issues.  This is a temporary workaround\n    until we can find the root cause.\n    '
    if hasattr(func, '__name__'):
        func_name = func.__name__
    elif hasattr(func, 'func'):
        func_name = getattr(func.func, '__name__', '__unknown__')
    else:
        func_name = '__unknown__'
    metrics_key = 'filestore.gcs.retry'
    metrics_tags = {
        'function': func_name,
    }
    idx = 0
    while True:
        try:
            result = func()
            metrics_tags.update({
                'success': '1',
            })
            metrics.timing(metrics_key, idx, tags=metrics_tags)
            return result
        except (DataCorruption, TransportError, RequestException) as e:
            if (idx >= GCS_RETRIES):
                metrics_tags.update({
                    'success': '0',
                    'exception_class': e.__class__.__name__,
                })
                metrics.timing(metrics_key, idx, tags=metrics_tags)
                raise
        idx += 1
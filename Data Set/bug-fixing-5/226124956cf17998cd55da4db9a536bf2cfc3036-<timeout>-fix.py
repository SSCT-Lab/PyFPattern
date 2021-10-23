def timeout(seconds=None, error_message='Timer expired'):
    if (seconds is None):
        seconds = (globals().get('GATHER_TIMEOUT') or 10)

    def decorator(func):

        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    if callable(seconds):
        func = seconds
        seconds = 10
        return decorator(func)
    else:
        return decorator
    return decorator
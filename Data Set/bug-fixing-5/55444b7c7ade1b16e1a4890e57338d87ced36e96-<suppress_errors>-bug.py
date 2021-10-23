def suppress_errors(func):

    def inner(*a, **k):
        try:
            return func(*a, **k)
        except Exception:
            capture_exception()
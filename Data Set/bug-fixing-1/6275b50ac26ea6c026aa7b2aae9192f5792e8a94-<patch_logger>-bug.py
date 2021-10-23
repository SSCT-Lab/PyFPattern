

@contextmanager
def patch_logger(logger_name, log_level, log_kwargs=False):
    '\n    Context manager that takes a named logger and the logging level\n    and provides a simple mock-like list of messages received.\n\n    Use unitttest.assertLogs() if you only need Python 3 support. This\n    private API will be removed after Python 2 EOL in 2020 (#27753).\n    '
    calls = []

    def replacement(msg, *args, **kwargs):
        call = (msg % args)
        calls.append(((call, kwargs) if log_kwargs else call))
    logger = logging.getLogger(logger_name)
    orig = getattr(logger, log_level)
    setattr(logger, log_level, replacement)
    try:
        (yield calls)
    finally:
        setattr(logger, log_level, orig)

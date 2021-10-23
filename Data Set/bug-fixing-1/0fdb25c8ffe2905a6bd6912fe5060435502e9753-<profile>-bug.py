

@contextlib.contextmanager
def profile():
    'Enable CUDA profiling during with statement.\n\n    This function enable profiling on entering with statement, and disable\n    profiling on leaving the statement.\n\n    >>> with cupy.cuda.profile():\n    ...    # do something you want to measure\n\n    '
    profiler.start()
    try:
        (yield)
    finally:
        profiler.stop()

def time_limited(timeout=0.5, return_val=np.nan, use_sigalrm=True):
    '\n    Decorator for setting a timeout for pure-Python functions.\n\n    If the function does not return within `timeout` seconds, the\n    value `return_val` is returned instead.\n\n    On POSIX this uses SIGALRM by default. On non-POSIX, settrace is\n    used. Do not use this with threads: the SIGALRM implementation\n    does probably not work well. The settrace implementation only\n    traces the current thread.\n\n    The settrace implementation slows down execution speed. Slowdown\n    by a factor around 10 is probably typical.\n    '
    if (POSIX and use_sigalrm):

        def sigalrm_handler(signum, frame):
            raise TimeoutError()

        def deco(func):

            def wrap(*a, **kw):
                old_handler = signal.signal(signal.SIGALRM, sigalrm_handler)
                signal.setitimer(signal.ITIMER_REAL, timeout)
                try:
                    return func(*a, **kw)
                except TimeoutError:
                    return return_val
                finally:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old_handler)
            return wrap
    else:

        def deco(func):

            def wrap(*a, **kw):
                start_time = time.time()

                def trace(frame, event, arg):
                    if ((time.time() - start_time) > timeout):
                        raise TimeoutError()
                    return None
                sys.settrace(trace)
                try:
                    return func(*a, **kw)
                except TimeoutError:
                    sys.settrace(None)
                    return return_val
                finally:
                    sys.settrace(None)
            return wrap
    return deco
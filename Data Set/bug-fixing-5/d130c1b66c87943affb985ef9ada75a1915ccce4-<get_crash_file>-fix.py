def get_crash_file(stacktrace):
    default = None
    for frame in reversed((get_path(stacktrace, 'frames', filter=True) or ())):
        fn = (frame.get('filename') or frame.get('abs_path'))
        if fn:
            if frame.get('in_app'):
                return fn
            if (default is None):
                default = fn
    return default


def _call_location():
    'Returns call location given level up from current call.'
    frame = inspect.currentframe()
    if frame:
        frame = frame.f_back
        frame = frame.f_back
        return ('%s:%d' % (frame.f_code.co_filename, frame.f_lineno))
    else:
        stack = inspect.stack(0)
        entry = stack[2]
        return ('%s:%d' % (entry[1], entry[2]))

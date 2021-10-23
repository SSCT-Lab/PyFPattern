def _call_location():
    'Returns call location given level up from current call.'
    frame = inspect.currentframe()
    if frame:
        first_frame = frame.f_back
        second_frame = first_frame.f_back
        frame = (second_frame if second_frame else first_frame)
        return ('%s:%d' % (frame.f_code.co_filename, frame.f_lineno))
    else:
        stack = inspect.stack(0)
        entry = stack[2]
        return ('%s:%d' % (entry[1], entry[2]))
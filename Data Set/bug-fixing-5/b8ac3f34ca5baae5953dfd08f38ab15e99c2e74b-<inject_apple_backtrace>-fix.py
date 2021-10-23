def inject_apple_backtrace(data, frames, diagnosis=None, error=None, system=None):
    app_uuid = None
    if system:
        app_uuid = system.get('app_uuid')
        if (app_uuid is not None):
            app_uuid = app_uuid.lower()
    converted_frames = []
    longest_addr = 0
    for frame in reversed(frames):
        fn = frame.get('filename')
        in_app = False
        if (app_uuid is not None):
            frame_uuid = frame.get('uuid')
            if (frame_uuid == app_uuid):
                in_app = True
        function = (frame['symbol_name'] or '<unknown>')
        lineno = frame.get('line')
        offset = None
        if (not lineno):
            offset = (frame['instruction_addr'] - frame['symbol_addr'])
        cframe = {
            'in_app': in_app,
            'abs_path': fn,
            'filename': ((fn and posixpath.basename(fn)) or None),
            'function': function,
            'package': frame['object_name'],
            'symbol_addr': ('%x' % frame['symbol_addr']),
            'instruction_addr': ('%x' % frame['instruction_addr']),
            'instruction_offset': offset,
            'lineno': lineno,
        }
        converted_frames.append(cframe)
        longest_addr = max(longest_addr, len(cframe['symbol_addr']), len(cframe['instruction_addr']))
    for frame in converted_frames:
        for key in ('symbol_addr', 'instruction_addr'):
            frame[key] = ('0x' + frame[key][2:].rjust(longest_addr, '0'))
    stacktrace = {
        'frames': converted_frames,
    }
    if (error or diagnosis):
        error = (error or {
            
        })
        exc = exception_from_apple_error_or_diagnosis(error, diagnosis)
        if (exc is not None):
            exc['stacktrace'] = stacktrace
            data['sentry.interfaces.Exception'] = {
                'values': [exc],
            }
            data['type'] = 'error'
            return
    data['sentry.interfaces.Stacktrace'] = stacktrace
def record_no_symsynd(data):
    if data.get('sentry.interfaces.AppleCrashReport'):
        append_error(data, {
            'type': EventError.NATIVE_NO_SYMSYND,
        })
        return data
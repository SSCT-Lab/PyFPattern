def record_no_symsynd(data):
    append_error(data, {
        'type': EventError.NATIVE_NO_SYMSYND,
    })
    return data
def to_lines(stdout):
    for item in stdout:
        if isinstance(item, string_types):
            item = to_native(item, errors='surrogate_or_strict').split('\n')
        (yield item)
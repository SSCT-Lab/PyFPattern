def get_config(module, flags=None):
    flags = to_list(flags)
    section_filter = False
    if (flags and ('section' in flags[(- 1)])):
        section_filter = True
    flag_str = ' '.join(flags)
    try:
        return _DEVICE_CONFIGS[flag_str]
    except KeyError:
        connection = get_connection(module)
        try:
            out = connection.get_config(flags=flags)
        except ConnectionError as exc:
            if section_filter:
                out = get_config(module, flags=flags[:(- 1)])
            else:
                module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
        cfg = to_text(out, errors='surrogate_then_replace').strip()
        _DEVICE_CONFIGS[flag_str] = cfg
        return cfg
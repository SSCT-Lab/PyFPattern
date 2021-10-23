def get_config(module, flags=None):
    flags = ([] if (flags is None) else flags)
    passwords = module.params['passwords']
    if passwords:
        cmd = 'more system:running-config'
    else:
        cmd = 'show running-config '
        cmd += ' '.join(flags)
        cmd = cmd.strip()
    try:
        return _DEVICE_CONFIGS[cmd]
    except KeyError:
        conn = get_connection(module)
        out = conn.get(cmd)
        cfg = to_text(out, errors='surrogate_then_replace').strip()
        _DEVICE_CONFIGS[cmd] = cfg
        return cfg
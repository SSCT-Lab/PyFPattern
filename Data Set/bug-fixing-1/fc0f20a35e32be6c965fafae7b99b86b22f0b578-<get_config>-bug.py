

def get_config(module):
    global _DEVICE_CONFIGS
    if (_DEVICE_CONFIGS != {
        
    }):
        return _DEVICE_CONFIGS
    else:
        connection = get_connection(module)
        try:
            out = connection.get_config()
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
        cfg = to_text(out, errors='surrogate_then_replace').strip()
        _DEVICE_CONFIGS = cfg
        return cfg

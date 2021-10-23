def get_connection(module):
    global _DEVICE_CONNECTION
    if (not _DEVICE_CONNECTION):
        load_params(module)
        if is_eapi(module):
            conn = Eapi(module)
        else:
            conn = Cli(module)
        _DEVICE_CONNECTION = conn
    return _DEVICE_CONNECTION
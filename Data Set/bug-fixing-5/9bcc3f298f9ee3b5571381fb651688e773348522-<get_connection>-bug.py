def get_connection(module):
    global _DEVICE_CONNECTION
    if (not _DEVICE_CONNECTION):
        load_params(module)
        transport = module.params['transport']
        provider_transport = (module.params['provider'] or {
            
        }).get('transport')
        if ('eapi' in (transport, provider_transport)):
            conn = Eapi(module)
        else:
            conn = Cli(module)
        _DEVICE_CONNECTION = conn
    return _DEVICE_CONNECTION
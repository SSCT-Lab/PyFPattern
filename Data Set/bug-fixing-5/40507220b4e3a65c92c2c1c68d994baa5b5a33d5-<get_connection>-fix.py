def get_connection(module):
    global _CONNECTION
    if _CONNECTION:
        return _CONNECTION
    _CONNECTION = Connection(module._socket_path)
    context = module.params.get('context')
    if context:
        if (context == 'system'):
            command = 'changeto system'
        else:
            command = ('changeto context %s' % context)
        _CONNECTION.get(command)
    return _CONNECTION
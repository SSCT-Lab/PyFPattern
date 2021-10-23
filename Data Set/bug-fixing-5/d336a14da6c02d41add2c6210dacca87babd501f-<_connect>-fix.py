def _connect(self, module):
    host = get_param(module, 'host')
    kwargs = {
        'port': (get_param(module, 'port') or 830),
        'user': get_param(module, 'username'),
    }
    if get_param(module, 'password'):
        kwargs['passwd'] = get_param(module, 'password')
    if get_param(module, 'ssh_keyfile'):
        kwargs['ssh_private_key_file'] = get_param(module, 'ssh_keyfile')
    kwargs['gather_facts'] = False
    try:
        device = Device(host, **kwargs)
        device.open()
        device.timeout = (get_param(module, 'timeout') or 10)
    except ConnectError as exc:
        module.fail_json(('unable to connect to %s: %s' % (host, to_text(exc))))
    return device
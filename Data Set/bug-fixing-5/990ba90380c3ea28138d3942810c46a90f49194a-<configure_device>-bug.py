def configure_device(module, warnings):
    candidate = (module.params['lines'] or module.params['src'])
    if isinstance(candidate, string_types):
        candidate = candidate.split('\n')
    kwargs = {
        'comment': module.params['comment'],
        'commit': (not module.check_mode),
    }
    if (module.params['confirm'] > 0):
        kwargs.update({
            'confirm': True,
            'confirm_timeout': module.params['confirm'],
        })
    config_format = None
    if module.params['src']:
        config_format = (module.params['src_format'] or guess_format(str(candidate)))
        if (config_format == 'set'):
            kwargs.update({
                'format': 'text',
                'action': 'set',
            })
        else:
            kwargs.update({
                'format': config_format,
                'action': module.params['update'],
            })
    if any((module.params['lines'], (config_format == 'set'))):
        candidate = filter_delete_statements(module, candidate)
        kwargs['format'] = 'text'
        kwargs['action'] = 'set'
    return load_config(module, candidate, warnings, **kwargs)
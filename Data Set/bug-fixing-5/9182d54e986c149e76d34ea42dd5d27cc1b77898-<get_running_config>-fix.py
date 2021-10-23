def get_running_config(module):
    contents = module.params['config']
    if (not contents):
        flags = []
        if module.params['defaults']:
            flags.append('include-default')
        contents = get_config(module, flags=flags)
    return NetworkConfig(indent=1, contents=contents)
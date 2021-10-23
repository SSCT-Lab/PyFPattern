

def get_running_config(module, config=None):
    contents = module.params['running_config']
    if (not contents):
        if config:
            contents = config
        else:
            flags = []
            if module.params['defaults']:
                flags.append('all')
            contents = get_config(module, flags=flags)
    return NetworkConfig(indent=3, contents=contents)

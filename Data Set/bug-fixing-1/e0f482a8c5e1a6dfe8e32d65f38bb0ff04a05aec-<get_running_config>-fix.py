

def get_running_config(module, config=None):
    contents = module.params['running_config']
    if (not contents):
        if ((not module.params['defaults']) and config):
            contents = config
        else:
            flags = ['all']
            contents = get_config(module, flags=flags)
    return NetworkConfig(indent=2, contents=contents)

def get_config(module, flags):
    cfg = get_cli_config(module, flags)
    config = (cfg.strip() if cfg else '')
    if config.startswith('display'):
        configs = config.split('\n')
        if (len(configs) > 1):
            return '\n'.join(configs[1:])
        else:
            return ''
    else:
        return config
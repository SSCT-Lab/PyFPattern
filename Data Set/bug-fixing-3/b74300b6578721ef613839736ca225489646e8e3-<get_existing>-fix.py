def get_existing(module, args):
    existing = {
        
    }
    netcfg = CustomNetworkConfig(indent=2, contents=get_config(module))
    if (module.params['interface'].startswith('loopback') or module.params['interface'].startswith('port-channel')):
        parents = ['interface {0}'.format(module.params['interface'])]
    else:
        parents = ['interface {0}'.format(module.params['interface'].capitalize())]
    config = netcfg.get_section(parents)
    if ('ospf' in config):
        for arg in args:
            if (arg not in ['interface']):
                existing[arg] = get_value(arg, config, module)
        existing['interface'] = module.params['interface']
    return existing
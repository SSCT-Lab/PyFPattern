def get_existing(module, args):
    existing = {
        
    }
    netcfg = get_config(module)
    custom = ['assoc_vrf', 'peer_list']
    interface_exist = check_interface(module, netcfg)
    if interface_exist:
        parents = ['interface {0}'.format(interface_exist)]
        temp_config = netcfg.get_section(parents)
        if ('member vni {0} associate-vrf'.format(module.params['vni']) in temp_config):
            parents.append('member vni {0} associate-vrf'.format(module.params['vni']))
            config = netcfg.get_section(parents)
        elif ('member vni {0}'.format(module.params['vni']) in temp_config):
            parents.append('member vni {0}'.format(module.params['vni']))
            config = netcfg.get_section(parents)
        else:
            config = {
                
            }
        if config:
            for arg in args:
                if (arg not in ['interface', 'vni']):
                    if (arg in custom):
                        existing[arg] = get_custom_value(arg, config, module)
                    else:
                        existing[arg] = get_value(arg, config, module)
            existing['interface'] = interface_exist
            existing['vni'] = module.params['vni']
    return (existing, interface_exist)
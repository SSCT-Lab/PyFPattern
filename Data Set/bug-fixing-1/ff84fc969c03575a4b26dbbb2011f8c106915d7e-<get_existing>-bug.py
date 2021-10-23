

def get_existing(module, args):
    existing = {
        
    }
    config = str(get_config(module))
    address = module.params['rp_address']
    pim_address_re = 'ip pim rp-address (?P<value>.*)$'
    for line in re.findall(pim_address_re, config, re.M):
        values = line.split()
        if (values[0] != address):
            continue
        existing['bidir'] = (existing.get('bidir') or ('bidir' in line))
        if (len(values) > 2):
            value = values[1]
            if (values[2] == 'route-map'):
                existing['route_map'] = value
            elif (values[2] == 'prefix-list'):
                existing['prefix_list'] = value
            elif (values[2] == 'group-list'):
                existing['group_list'] = value
    return existing

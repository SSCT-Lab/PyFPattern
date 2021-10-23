

def get_existing(module, args, warnings):
    existing = {
        
    }
    netcfg = CustomNetworkConfig(indent=2, contents=get_config(module))
    asn_re = re.compile('.*router\\sbgp\\s(?P<existing_asn>\\d+).*', re.S)
    asn_match = asn_re.match(str(netcfg))
    if asn_match:
        existing_asn = asn_match.group('existing_asn')
        bgp_parent = 'router bgp {0}'.format(existing_asn)
        if (module.params['vrf'] != 'default'):
            parents = [bgp_parent, 'vrf {0}'.format(module.params['vrf'])]
        else:
            parents = [bgp_parent]
        config = netcfg.get_section(parents)
        if config:
            for arg in args:
                if ((arg != 'asn') and ((module.params['vrf'] == 'default') or (arg not in GLOBAL_PARAMS))):
                    existing[arg] = get_value(arg, config)
            existing['asn'] = existing_asn
            if (module.params['vrf'] == 'default'):
                existing['vrf'] = 'default'
    if ((not existing) and (module.params['vrf'] != 'default') and (module.params['state'] == 'present')):
        msg = "VRF {0} doesn't exist.".format(module.params['vrf'])
        warnings.append(msg)
    return existing

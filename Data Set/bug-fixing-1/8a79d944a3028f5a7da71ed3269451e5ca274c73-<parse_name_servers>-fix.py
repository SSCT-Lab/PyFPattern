

def parse_name_servers(config, vrf_config, vrfs):
    objects = list()
    match = re.search('^ip name-server (.+)$', config, re.M)
    if (match and ('use-vrf' not in match.group(1))):
        for addr in match.group(1).split(' '):
            objects.append({
                'server': addr,
                'vrf': None,
            })
    for (vrf, cfg) in iteritems(vrf_config):
        vrf_match = re.search('ip name-server (.+)', cfg, re.M)
        if vrf_match:
            for addr in vrf_match.group(1).split(' '):
                objects.append({
                    'server': addr,
                    'vrf': vrf,
                })
    return objects

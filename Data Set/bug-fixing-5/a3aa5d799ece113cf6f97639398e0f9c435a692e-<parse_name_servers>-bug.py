def parse_name_servers(config, vrf_config):
    objects = list()
    match = re.search('^ip name-server (.+)$', config, re.M)
    if match:
        for addr in match.group(1).split(' '):
            objects.append({
                'server': addr,
                'vrf': None,
            })
    for (vrf, cfg) in iteritems(vrf_config):
        for item in re.findall('ip name-server (\\S+)', cfg, re.M):
            for addr in match.group(1).split(' '):
                objects.append({
                    'server': addr,
                    'vrf': vrf,
                })
    return objects
def parse_name_servers(config):
    match = re.findall('^ip name-server (?:vrf (\\S+) )*(\\S+)', config, re.M)
    matches = list()
    for (vrf, server) in match:
        if (not vrf):
            vrf = None
        matches.append({
            'server': server,
            'vrf': vrf,
        })
    return matches
def parse_name_servers(config):
    match = re.findall('^ip name-server (?:vrf (\\S+) )*(.*)', config, re.M)
    matches = list()
    for (vrf, servers) in match:
        if (not vrf):
            vrf = None
        for server in servers.split():
            matches.append({
                'server': server,
                'vrf': vrf,
            })
    return matches
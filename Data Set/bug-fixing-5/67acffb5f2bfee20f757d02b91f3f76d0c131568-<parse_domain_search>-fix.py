def parse_domain_search(config):
    match = re.findall('^ip domain[- ]list (?:vrf (\\S+) )*(\\S+)', config, re.M)
    matches = list()
    for (vrf, name) in match:
        if (not vrf):
            vrf = None
        matches.append({
            'name': name,
            'vrf': vrf,
        })
    return matches
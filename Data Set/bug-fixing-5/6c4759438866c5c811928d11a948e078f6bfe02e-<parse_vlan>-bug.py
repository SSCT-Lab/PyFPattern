def parse_vlan(self, vlan):
    facts = dict()
    (vlan_info, vlan_info_next) = vlan.split('----------   -----   --------------- --------------- -------')
    for en in vlan_info_next.splitlines():
        if (en == ''):
            continue
        match = re.search('^(\\S+)\\s+(\\S+)\\s+(\\S+)', en)
        intf = match.group(1)
        if (intf not in facts):
            facts[intf] = list()
        fact = dict()
        matc = re.search('^([\\w+\\s\\d]*)\\s+(\\S+)\\s+(\\S+)', en)
        fact['address'] = matc.group(2)
        fact['masklen'] = matc.group(3)
        facts[intf].append(fact)
    return facts
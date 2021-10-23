def populate_neighbors_cdp(self, data):
    facts = dict()
    for item in data.split('----------------------------------------'):
        if (item == ''):
            continue
        local_intf = self.parse_lldp_intf(item)
        if (local_intf not in facts):
            facts[local_intf] = list()
        fact = dict()
        fact['port'] = self.parse_lldp_port(item)
        fact['sysname'] = self.parse_lldp_sysname(item)
        facts[local_intf].append(facts)
    return facts
def parse_neighbors(self, neighbors):
    facts = dict()
    for entry in neighbors.split('------------------------------------------------'):
        if (entry == ''):
            continue
        intf = self.parse_lldp_intf(entry)
        if (intf not in facts):
            facts[intf] = list()
        fact = dict()
        fact['host'] = self.parse_lldp_host(entry)
        fact['port'] = self.parse_lldp_port(entry)
        facts[intf].append(fact)
    return facts
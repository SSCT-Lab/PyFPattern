def parse_neighbors(self, neighbors):
    facts = dict()
    nbors = neighbors.split('------------------------------------------------')
    for entry in nbors[1:]:
        if (entry == ''):
            continue
        intf = self.parse_lldp_intf(entry)
        if (intf not in facts):
            facts[intf] = list()
        fact = dict()
        fact['host'] = self.parse_lldp_host(entry)
        fact['remote_description'] = self.parse_lldp_remote_desc(entry)
        fact['port'] = self.parse_lldp_port(entry)
        facts[intf].append(fact)
    return facts
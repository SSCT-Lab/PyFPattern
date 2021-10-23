def parse_vlan(self, vlan, version_info):
    facts = dict()
    if ('N11' in version_info):
        match = re.search('IP Address(.+)\\s([0-9.]*)\\n', vlan)
        mask = re.search('Subnet Mask(.+)\\s([0-9.]*)\\n', vlan)
        vlan_id_match = re.search('Management VLAN ID(.+)\\s(\\d+)', vlan)
        vlan_id = ('Vl' + vlan_id_match.group(2))
        if (vlan_id not in facts):
            facts[vlan_id] = list()
        fact = dict()
        fact['address'] = match.group(2)
        fact['masklen'] = mask.group(2)
        facts[vlan_id].append(fact)
    else:
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


def parse_lldp_intf(self, data):
    match = re.search('Interface:\\s*(\\S+)', data, re.M)
    if match:
        return match.group(1)

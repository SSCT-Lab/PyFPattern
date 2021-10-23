def parse_lineprotocol(self, data):
    match = re.search('line protocol is (.+)$', data, re.M)
    if match:
        return match.group(1)


def parse_duplex(self, data):
    match = re.search('(\\w+) Duplex', data, re.M)
    if match:
        return match.group(1)

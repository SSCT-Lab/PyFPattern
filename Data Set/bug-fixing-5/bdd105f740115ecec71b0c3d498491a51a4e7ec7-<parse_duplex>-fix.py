def parse_duplex(self, data):
    match = re.search('(\\w+)(?: D|-d)uplex', data, re.M)
    if match:
        return match.group(1)
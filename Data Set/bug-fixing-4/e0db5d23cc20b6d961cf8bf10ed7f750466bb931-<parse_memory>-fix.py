def parse_memory(self, data):
    return re.findall('(\\d+)', data, re.M)
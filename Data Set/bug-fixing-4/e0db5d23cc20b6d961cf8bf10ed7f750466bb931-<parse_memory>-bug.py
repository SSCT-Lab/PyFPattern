def parse_memory(self, data):
    return re.findall('\\:\\s*(\\d+)', data, re.M)
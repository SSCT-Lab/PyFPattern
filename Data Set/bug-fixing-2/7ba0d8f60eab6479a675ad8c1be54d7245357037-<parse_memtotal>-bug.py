

def parse_memtotal(self, data):
    match = re.search('TotalMemory: (\\d+)\\s', data, re.M)
    if match:
        return match.group(1)

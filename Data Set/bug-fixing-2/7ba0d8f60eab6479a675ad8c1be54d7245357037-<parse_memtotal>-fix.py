

def parse_memtotal(self, data):
    match = re.search('Total\\s*Memory: (\\d+)\\s', data, re.M)
    if match:
        return match.group(1)

def parse_serialnum(self, data):
    match = re.search('board ID (\\S+)', data)
    if match:
        return match.group(1)
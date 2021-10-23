def parse_serialnum(self, data):
    match = re.findall('^System serial number\\s+: (\\S+)', data, re.M)
    if match:
        return match
    else:
        match = re.search('board ID (\\S+)', data)
        if match:
            return [match.group(1)]
def parse_model(self, data):
    match = re.search('^Cisco (.+) \\(revision', data, re.M)
    if match:
        return match.group(1)
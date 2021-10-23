def parse_version(self, data):
    match = re.search('Version (\\S+),', data)
    if match:
        return match.group(1)
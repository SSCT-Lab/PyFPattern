def parse_hostname(self, data):
    match = re.search('hostname\\s+(\\S+)', data, re.M)
    if match:
        return match.group(1)
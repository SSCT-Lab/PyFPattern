def parse_version(self, data):
    match = re.search('HW Version(.+)\\s(\\d+)', data)
    if match:
        return match.group(2)
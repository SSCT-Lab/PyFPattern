def parse_macaddress(self, data):
    match = re.search('Burned MAC Address(.+)\\s([A-Z0-9.]*)\\n', data)
    if match:
        return match.group(2)
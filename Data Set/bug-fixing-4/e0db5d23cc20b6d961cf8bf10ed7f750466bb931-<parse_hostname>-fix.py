def parse_hostname(self, data):
    hostname = data.find('./data/system-state/system-status/hostname')
    if (hostname is not None):
        return hostname.text
    else:
        return ''
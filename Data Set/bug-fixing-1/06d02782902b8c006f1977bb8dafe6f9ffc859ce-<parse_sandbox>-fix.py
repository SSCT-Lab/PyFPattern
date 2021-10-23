

def parse_sandbox(data):
    match = re.search('Sandbox:\\s+(.+)$', data, re.M)
    value = None
    if match:
        value = (match.group(1) == 'Enabled')
    return {
        'sandbox': value,
    }

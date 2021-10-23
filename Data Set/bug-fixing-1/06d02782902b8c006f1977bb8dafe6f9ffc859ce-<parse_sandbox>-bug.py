

def parse_sandbox(data):
    match = re.search('Sandbox:\\s+(.+)$', data, re.M)
    return {
        'sandbox': (match.group(1) == 'Enabled'),
    }

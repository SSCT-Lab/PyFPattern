def _expand_hostpattern(self, hostpattern):
    '\n        Takes a single host pattern and returns a list of hostnames and an\n        optional port number that applies to all of them.\n        '
    try:
        (pattern, port) = parse_address(hostpattern, allow_ranges=True)
    except:
        pattern = hostpattern
        port = None
    if detect_range(pattern):
        hostnames = expand_hostname_range(pattern)
    else:
        hostnames = [pattern]
    return (hostnames, port)
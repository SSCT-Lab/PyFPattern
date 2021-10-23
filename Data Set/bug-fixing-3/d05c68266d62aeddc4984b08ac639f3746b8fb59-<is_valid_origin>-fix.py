def is_valid_origin(origin, project=None, allowed=None):
    '\n    Given an ``origin`` which matches a base URI (e.g. http://example.com)\n    determine if a valid origin is present in the project settings.\n\n    Origins may be defined in several ways:\n\n    - http://domain.com[:port]: exact match for base URI (must include port)\n    - *: allow any domain\n    - *.domain.com: matches domain.com and all subdomains, on any port\n    - domain.com: matches domain.com on any port\n    - *:port: wildcard on hostname, but explicit match on port\n    '
    if (allowed is None):
        allowed = get_origins(project)
    if (not allowed):
        return False
    if ('*' in allowed):
        return True
    if (not origin):
        return False
    origin = origin.lower()
    if (origin in allowed):
        return True
    if (origin == 'null'):
        return False
    if isinstance(origin, six.binary_type):
        try:
            origin = origin.decode('utf-8')
        except UnicodeDecodeError:
            try:
                origin = origin.decode('windows-1252')
            except UnicodeDecodeError:
                return False
    parsed = urlparse(origin)
    if (parsed.hostname is None):
        parsed_hostname = ''
    else:
        try:
            parsed_hostname = parsed.hostname.encode('idna')
        except UnicodeError:
            parsed_hostname = parsed.hostname
    if parsed.port:
        domain_matches = ('*', parsed_hostname, ('%s:%d' % (parsed_hostname, parsed.port)), ('*:%d' % parsed.port))
    else:
        domain_matches = ('*', parsed_hostname)
    for value in allowed:
        try:
            bits = parse_uri_match(value)
        except UnicodeError:
            continue
        if (bits.scheme not in ('*', parsed.scheme)):
            continue
        if (bits.domain[:2] == '*.'):
            if (parsed_hostname.endswith(bits.domain[1:]) or (parsed_hostname == bits.domain[2:])):
                return True
            continue
        elif (bits.domain not in domain_matches):
            continue
        path = bits.path
        if (path == '*'):
            return True
        if path.endswith('*'):
            path = path[:(- 1)]
        if parsed.path.startswith(path):
            return True
    return False
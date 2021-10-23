def parse_uri_match(value):
    if ('://' in value):
        (scheme, value) = value.split('://', 1)
    else:
        scheme = '*'
    if ('/' in value):
        (domain, path) = value.split('/', 1)
    else:
        (domain, path) = (value, '*')
    if (':' in domain):
        (domain, port) = value.split(':', 1)
    else:
        port = None
    if isinstance(domain, six.binary_type):
        domain = domain.decode('utf8')
    domain = domain.encode('idna')
    if port:
        domain = ('%s:%s' % (domain, port))
    return ParsedUriMatch(scheme, domain, path)
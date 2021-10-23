@classmethod
def to_python(cls, data):
    (is_valid, errors) = validate_and_default_interface(data, cls.path)
    if (not is_valid):
        raise InterfaceValidationError('Invalid interface data')
    kwargs = {
        
    }
    if data.get('method'):
        method = data['method'].upper()
        if ((method not in ('GET', 'POST')) and (not http_method_re.match(method))):
            raise InterfaceValidationError("Invalid value for 'method'")
        kwargs['method'] = method
    else:
        kwargs['method'] = None
    if data.get('url', None):
        url = to_unicode(data['url'])
        if url.endswith('…'):
            url = (url[:(- 1)] + '...')
        (scheme, netloc, path, query_bit, fragment_bit) = urlsplit(url)
    else:
        scheme = netloc = path = query_bit = fragment_bit = None
    query_string = (data.get('query_string') or query_bit)
    if query_string:
        if isinstance(query_string, six.string_types):
            if (query_string[0] == '?'):
                query_string = query_string[1:]
            if query_string.endswith('…'):
                query_string = (query_string[:(- 1)] + '...')
            query_string = [(to_unicode(k), jsonify(v)) for (k, v) in parse_qsl(query_string, keep_blank_values=True)]
        elif isinstance(query_string, dict):
            query_string = [(to_unicode(k), jsonify(v)) for (k, v) in six.iteritems(query_string)]
        elif isinstance(query_string, list):
            query_string = [tuple(tup) for tup in query_string if (isinstance(tup, (tuple, list)) and (len(tup) == 2))]
        else:
            query_string = []
        kwargs['query_string'] = trim(query_string, 4096)
    else:
        kwargs['query_string'] = []
    fragment = (data.get('fragment') or fragment_bit)
    cookies = data.get('cookies')
    headers = data.get('headers')
    if headers:
        (headers, cookie_header) = format_headers(headers)
        if ((not cookies) and cookie_header):
            cookies = cookie_header
    else:
        headers = ()
    body = data.get('data')
    content_type = next((v for (k, v) in headers if (k == 'Content-Type')), None)
    if (content_type is not None):
        content_type = content_type.partition(';')[0].rstrip()
    inferred_content_type = data.get('inferred_content_type', content_type)
    if (('inferred_content_type' not in data) and (not isinstance(body, dict))):
        (body, inferred_content_type) = heuristic_decode(body, content_type)
    if body:
        body = trim(body, settings.SENTRY_MAX_HTTP_BODY_SIZE)
    env = data.get('env', {
        
    })
    if ('REMOTE_ADDR' in env):
        try:
            validate_ip(env['REMOTE_ADDR'], required=False)
        except ValueError:
            del env['REMOTE_ADDR']
    kwargs['inferred_content_type'] = inferred_content_type
    kwargs['cookies'] = trim_pairs(format_cookies(cookies))
    kwargs['env'] = trim_dict(env)
    kwargs['headers'] = trim_pairs(headers)
    kwargs['data'] = fix_broken_encoding(body)
    kwargs['url'] = urlunsplit((scheme, netloc, path, '', ''))
    kwargs['fragment'] = trim(fragment, 1024)
    return cls(**kwargs)
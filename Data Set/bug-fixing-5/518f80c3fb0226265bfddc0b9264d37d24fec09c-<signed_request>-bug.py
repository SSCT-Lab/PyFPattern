def signed_request(module=None, method='GET', service=None, host=None, uri=None, query=None, body='', headers=None, session_in_header=True, session_in_query=False):
    'Generate a SigV4 request to an AWS resource for a module\n\n    This is used if you wish to authenticate with AWS credentials to a secure endpoint like an elastisearch domain.\n\n    Returns :class:`HTTPResponse` object.\n\n    Example:\n        result = signed_request(\n            module=this,\n            service="es",\n            host="search-recipes1-xxxxxxxxx.us-west-2.es.amazonaws.com",\n        )\n\n    :kwarg host: endpoint to talk to\n    :kwarg service: AWS id of service (like `ec2` or `es`)\n    :kwarg module: An AnsibleAWSModule to gather connection info from\n\n    :kwarg body: (optional) Payload to send\n    :kwarg method: (optional) HTTP verb to use\n    :kwarg query: (optional) dict of query params to handle\n    :kwarg uri: (optional) Resource path without query parameters\n\n    :kwarg session_in_header: (optional) Add the session token to the headers\n    :kwarg session_in_query: (optional) Add the session token to the query parameters\n\n    :returns: HTTPResponse\n    '
    if (not HAS_BOTO3):
        module.fail_json('A sigv4 signed_request requires boto3')
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')
    algorithm = 'AWS4-HMAC-SHA256'
    (region, dummy, dummy) = get_aws_connection_info(module, boto3=True)
    credentials = get_aws_credentials_object(module)
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    session_token = credentials.token
    if (not access_key):
        module.fail_json(msg='aws_access_key_id is missing')
    if (not secret_key):
        module.fail_json(msg='aws_secret_access_key is missing')
    credential_scope = '/'.join([datestamp, region, service, 'aws4_request'])
    uri = (uri or '/')
    query_string = (format_querystring(query) if query else '')
    headers = (headers or dict())
    query = (query or dict())
    headers.update({
        'host': host,
        'x-amz-date': amz_date,
    })
    if session_token:
        if session_in_header:
            headers['X-Amz-Security-Token'] = session_token
        if session_in_query:
            query['X-Amz-Security-Token'] = session_token
    if (method is 'GET'):
        body = ''
    body = body
    body_hash = hexdigest(body)
    signed_headers = ';'.join(sorted(headers.keys()))
    cannonical_headers = ('\n'.join([((key.lower().strip() + ':') + value) for (key, value) in headers.items()]) + '\n')
    cannonical_request = '\n'.join([method, uri, query_string, cannonical_headers, signed_headers, body_hash])
    string_to_sign = '\n'.join([algorithm, amz_date, credential_scope, hexdigest(cannonical_request)])
    signing_key = get_signature_key(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = '{0} Credential={1}/{2}, SignedHeaders={3}, Signature={4}'.format(algorithm, access_key, credential_scope, signed_headers, signature)
    url = (('https://' + host) + uri)
    if (query_string is not ''):
        url = ((url + '?') + query_string)
    final_headers = {
        'x-amz-date': amz_date,
        'Authorization': authorization_header,
    }
    final_headers.update(headers)
    return open_url(url, method=method, data=body, headers=final_headers)
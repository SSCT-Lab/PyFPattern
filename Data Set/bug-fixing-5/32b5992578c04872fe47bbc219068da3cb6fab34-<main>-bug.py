def main():
    argument_spec = url_argument_spec()
    argument_spec.update(dict(dest=dict(type='path'), url_username=dict(type='str', aliases=['user']), url_password=dict(type='str', aliases=['password'], no_log=True), body=dict(type='raw'), body_format=dict(type='str', default='raw', choices=['form-urlencoded', 'json', 'raw']), src=dict(type='path'), method=dict(type='str', default='GET', choices=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH', 'TRACE', 'CONNECT', 'REFRESH']), return_content=dict(type='bool', default=False), follow_redirects=dict(type='str', default='safe', choices=['all', 'no', 'none', 'safe', 'urllib2', 'yes']), creates=dict(type='path'), removes=dict(type='path'), status_code=dict(type='list', default=[200]), timeout=dict(type='int', default=30), headers=dict(type='dict', default={
        
    })))
    module = AnsibleModule(argument_spec=argument_spec, check_invalid_arguments=False, add_file_common_args=True, mutually_exclusive=[['body', 'src']])
    url = module.params['url']
    body = module.params['body']
    body_format = module.params['body_format'].lower()
    method = module.params['method']
    dest = module.params['dest']
    return_content = module.params['return_content']
    creates = module.params['creates']
    removes = module.params['removes']
    status_code = [int(x) for x in list(module.params['status_code'])]
    socket_timeout = module.params['timeout']
    dict_headers = module.params['headers']
    if (body_format == 'json'):
        if (not isinstance(body, string_types)):
            body = json.dumps(body)
        if ('content-type' not in [header.lower() for header in dict_headers]):
            dict_headers['Content-Type'] = 'application/json'
    elif (body_format == 'form-urlencoded'):
        if (not isinstance(body, string_types)):
            try:
                body = form_urlencoded(body)
            except ValueError as e:
                module.fail_json(msg=('failed to parse body as form_urlencoded: %s' % to_native(e)))
        if ('content-type' not in [header.lower() for header in dict_headers]):
            dict_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    for (key, value) in iteritems(module.params):
        if key.startswith('HEADER_'):
            module.deprecate('Supplying headers via HEADER_* is deprecated. Please use `headers` to supply headers for the request', version='2.9')
            skey = key.replace('HEADER_', '')
            dict_headers[skey] = value
    if (creates is not None):
        if os.path.exists(creates):
            module.exit_json(stdout=("skipped, since '%s' exists" % creates), changed=False, rc=0)
    if (removes is not None):
        if (not os.path.exists(removes)):
            module.exit_json(stdout=("skipped, since '%s' does not exist" % removes), changed=False, rc=0)
    (resp, content, dest) = uri(module, url, dest, body, body_format, method, dict_headers, socket_timeout)
    resp['status'] = int(resp['status'])
    if (dest is not None):
        if (resp['status'] == 304):
            changed = False
        else:
            write_file(module, url, dest, content)
            changed = True
            module.params['path'] = dest
            file_args = module.load_file_common_arguments(module.params)
            file_args['path'] = dest
            changed = module.set_fs_attributes_if_different(file_args, changed)
        resp['path'] = dest
    else:
        changed = False
    uresp = {
        
    }
    for (key, value) in iteritems(resp):
        ukey = key.replace('-', '_').lower()
        uresp[ukey] = value
    try:
        uresp['location'] = absolute_location(url, uresp['location'])
    except KeyError:
        pass
    content_encoding = 'utf-8'
    if ('content_type' in uresp):
        (content_type, params) = cgi.parse_header(uresp['content_type'])
        if ('charset' in params):
            content_encoding = params['charset']
        u_content = to_text(content, encoding=content_encoding)
        if any(((candidate in content_type) for candidate in JSON_CANDIDATES)):
            try:
                js = json.loads(u_content)
                uresp['json'] = js
            except:
                pass
    else:
        u_content = to_text(content, encoding=content_encoding)
    if (resp['status'] not in status_code):
        uresp['msg'] = ('Status code was %s and not %s: %s' % (resp['status'], status_code, uresp.get('msg', '')))
        module.fail_json(content=u_content, **uresp)
    elif return_content:
        module.exit_json(changed=changed, content=u_content, **uresp)
    else:
        module.exit_json(changed=changed, **uresp)
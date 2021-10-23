def main():
    argument_spec = url_argument_spec()
    argument_spec.update(dict(dest=dict(required=False, default=None, type='path'), url_username=dict(required=False, default=None, aliases=['user']), url_password=dict(required=False, default=None, aliases=['password'], no_log=True), body=dict(required=False, default=None, type='raw'), body_format=dict(required=False, default='raw', choices=['raw', 'json']), method=dict(required=False, default='GET', choices=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH', 'TRACE', 'CONNECT', 'REFRESH']), return_content=dict(required=False, default='no', type='bool'), follow_redirects=dict(required=False, default='safe', choices=['all', 'safe', 'none', 'yes', 'no']), creates=dict(required=False, default=None, type='path'), removes=dict(required=False, default=None, type='path'), status_code=dict(required=False, default=[200], type='list'), timeout=dict(required=False, default=30, type='int'), headers=dict(required=False, type='dict', default={
        
    })))
    module = AnsibleModule(argument_spec=argument_spec, check_invalid_arguments=False, add_file_common_args=True)
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
        if (not isinstance(body, six.string_types)):
            body = json.dumps(body)
        lower_header_keys = [key.lower() for key in dict_headers]
        if ('content-type' not in lower_header_keys):
            dict_headers['Content-Type'] = 'application/json'
    for (key, value) in six.iteritems(module.params):
        if key.startswith('HEADER_'):
            skey = key.replace('HEADER_', '')
            dict_headers[skey] = value
    if (creates is not None):
        if os.path.exists(creates):
            module.exit_json(stdout=('skipped, since %s exists' % creates), changed=False, stderr=False, rc=0)
    if (removes is not None):
        if (not os.path.exists(removes)):
            module.exit_json(stdout=('skipped, since %s does not exist' % removes), changed=False, stderr=False, rc=0)
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
    for (key, value) in six.iteritems(resp):
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
        if (('application/json' in content_type) or ('text/json' in content_type)):
            try:
                js = json.loads(u_content)
                uresp['json'] = js
            except:
                pass
    else:
        u_content = to_text(content, encoding=content_encoding)
    if (resp['status'] not in status_code):
        uresp['msg'] = ('Status code was not %s: %s' % (status_code, uresp.get('msg', '')))
        module.fail_json(content=u_content, **uresp)
    elif return_content:
        module.exit_json(changed=changed, content=u_content, **uresp)
    else:
        module.exit_json(changed=changed, **uresp)
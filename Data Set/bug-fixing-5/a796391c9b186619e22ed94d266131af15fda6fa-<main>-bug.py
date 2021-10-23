def main():
    argument_spec = aci_argument_spec
    argument_spec.update(path=dict(type='str', required=True, aliases=['uri']), method=dict(type='str', default='get', choices=['delete', 'get', 'post'], aliases=['action']), src=dict(type='path', aliases=['config_file']), content=dict(type='str'))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['content', 'src']], supports_check_mode=True)
    path = module.params['path']
    content = module.params['content']
    src = module.params['src']
    method = module.params['method']
    timeout = module.params['timeout']
    file_exists = False
    if src:
        if os.path.isfile(src):
            file_exists = True
        else:
            module.fail_json(msg=("Cannot find/access src '%s'" % src))
    if (path.find('.xml') != (- 1)):
        rest_type = 'xml'
        if (not HAS_LXML_ETREE):
            module.fail_json(msg='The lxml python library is missing, or lacks etree support.')
        if (not HAS_XMLJSON_COBRA):
            module.fail_json(msg='The xmljson python library is missing, or lacks cobra support.')
    elif (path.find('.json') != (- 1)):
        rest_type = 'json'
    else:
        module.fail_json(msg='Failed to find REST API content type (neither .xml nor .json).')
    aci = ACIModule(module)
    if (method == 'get'):
        aci.request(path)
        module.exit_json(**aci.result)
    elif module.check_mode:
        aci.result['changed'] = True
        module.exit_json(response='OK (Check mode)', status=200, **aci.result)
    if content:
        payload = content
    elif file_exists:
        with open(src, 'r') as config_object:
            payload = config_object.read()
    url = (('%(protocol)s://%(hostname)s/' % aci.params) + path.lstrip('/'))
    (resp, info) = fetch_url(module, url, data=payload, method=method.upper(), timeout=timeout, headers=aci.headers)
    aci.result['response'] = info['msg']
    aci.result['status'] = info['status']
    if (info['status'] != 200):
        try:
            aci_response(aci.result, info['body'], rest_type)
            module.fail_json(msg=('Request failed: %(error_code)s %(error_text)s' % aci.result), **aci.result)
        except KeyError:
            module.fail_json(msg=('Request failed for %(url)s. %(msg)s' % info), **aci.result)
    aci_response(aci.result, resp.read(), rest_type)
    module.exit_json(**aci.result)
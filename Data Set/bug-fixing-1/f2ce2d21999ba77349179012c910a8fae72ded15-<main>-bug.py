

def main():
    module = AnsibleModule(argument_spec=dict(hostname=dict(type='str', required=True, aliases=['host', 'ip']), username=dict(type='str', default='admin', aliases=['user']), password=dict(type='str', default='password', no_log=True), content=dict(type='str'), path=dict(type='path', aliases=['config_file', 'src']), protocol=dict(type='str', default='https', choices=['http', 'https']), timeout=dict(type='int', default=30), validate_certs=dict(type='bool', default=True)), supports_check_mode=True, mutually_exclusive=[['content', 'path']])
    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    content = module.params['content']
    path = module.params['path']
    protocol = module.params['protocol']
    timeout = module.params['timeout']
    result = dict(failed=False, changed=False)
    file_exists = False
    if path:
        if os.path.isfile(path):
            file_exists = True
        else:
            module.fail_json(msg=('Cannot find/access path:\n%s' % path))
    url = ('%s://%s/nuova' % (protocol, hostname))
    data = ('<aaaLogin inName="%s" inPassword="%s"/>' % (username, password))
    (resp, auth) = fetch_url(module, url, data=data, method='POST', timeout=timeout)
    if ((resp is None) or (auth['status'] != 200)):
        module.fail_json(msg=('Task failed with error %(status)s: %(msg)s' % auth), **result)
    result.update(imc_response(module, resp.read()))
    try:
        cookie = result['aaaLogin']['attributes']['outCookie']
    except:
        module.fail_json(msg='Could not find cookie in output', **result)
    atexit.register(logout, module, url, cookie, timeout)
    if content:
        rawdata = content
    elif file_exists:
        with open(path, 'r') as config_object:
            rawdata = config_object.read()
    xmldata = lxml.etree.fromstring(('<root>%s</root>' % rawdata.replace('\n', '')))
    for xmldoc in list(xmldata):
        if (xmldoc.tag is lxml.etree.Comment):
            continue
        xmldoc.set('cookie', cookie)
        data = lxml.etree.tostring(xmldoc)
        (resp, info) = fetch_url(module, url, data=data, method='POST', timeout=timeout)
        if ((resp is None) or (auth['status'] != 200)):
            module.fail_json(msg=('Task failed with error %(status)s: %(msg)s' % auth), **result)
        rawoutput = resp.read()
        result = merge(result, imc_response(module, rawoutput, rawinput=data))
        result['response'] = info['msg']
        result['status'] = info['status']
        xmloutput = lxml.etree.fromstring(rawoutput)
        results = xmloutput.xpath('/configConfMo/outConfig/*/@status')
        result['changed'] = ('modified' in results)
    module.exit_json(**result)

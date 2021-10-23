def main():
    module = AnsibleModule(argument_spec=dict(script=dict(required=True, type='str'), url=dict(required=False, type='str', default='http://localhost:8080'), validate_certs=dict(required=False, type='bool', default=True), user=dict(required=False, no_log=True, type='str', default=None), password=dict(required=False, no_log=True, type='str', default=None), args=dict(required=False, type='dict', default=None)))
    if (module.params['user'] is not None):
        if (module.params['password'] is None):
            module.fail_json(msg='password required when user provided')
        module.params['url_username'] = module.params['user']
        module.params['url_password'] = module.params['password']
        module.params['force_basic_auth'] = True
    if (module.params['args'] is not None):
        from string import Template
        script_contents = Template(module.params['script']).substitute(module.params['args'])
    else:
        script_contents = module.params['script']
    headers = {
        
    }
    if is_csrf_protection_enabled(module):
        crumb = get_crumb(module)
        headers = {
            crumb['crumbRequestField']: crumb['crumb'],
        }
    (resp, info) = fetch_url(module, (module.params['url'] + '/scriptText'), data=urlencode({
        'script': script_contents,
    }), headers=headers, method='POST')
    if (info['status'] != 200):
        module.fail_json(msg=((('HTTP error ' + str(info['status'])) + ' ') + info['msg']))
    result = resp.read()
    if (('Exception:' in result) and ('at java.lang.Thread' in result)):
        module.fail_json(msg=('script failed with stacktrace:\n ' + result))
    module.exit_json(output=result)
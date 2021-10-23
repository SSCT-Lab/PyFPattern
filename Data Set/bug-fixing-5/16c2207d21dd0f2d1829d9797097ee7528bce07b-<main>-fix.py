def main():
    module = AnsibleModule(argument_spec=dict(token=dict(required=True, no_log=True), environment=dict(required=True), user=dict(required=False), repo=dict(required=False), revision=dict(required=False), url=dict(required=False, default='https://api.honeybadger.io/v1/deploys'), validate_certs=dict(default='yes', type='bool')), supports_check_mode=True)
    params = {
        
    }
    if module.params['environment']:
        params['deploy[environment]'] = module.params['environment']
    if module.params['user']:
        params['deploy[local_username]'] = module.params['user']
    if module.params['repo']:
        params['deploy[repository]'] = module.params['repo']
    if module.params['revision']:
        params['deploy[revision]'] = module.params['revision']
    params['api_key'] = module.params['token']
    url = module.params.get('url')
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        data = urlencode(params)
        (response, info) = fetch_url(module, url, data=data)
    except Exception:
        e = get_exception()
        module.fail_json(msg=('Unable to notify Honeybadger: %s' % e))
    else:
        if (info['status'] == 201):
            module.exit_json(changed=True)
        else:
            module.fail_json(msg=('HTTP result code: %d connecting to %s' % (info['status'], url)))
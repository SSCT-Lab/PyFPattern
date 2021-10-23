

def main():
    module = AnsibleModule(argument_spec=dict(token=dict(required=True), environment=dict(required=True), revision=dict(required=True), user=dict(required=False), rollbar_user=dict(required=False), comment=dict(required=False), url=dict(required=False, default='https://api.rollbar.com/api/1/deploy/'), validate_certs=dict(default='yes', type='bool')), supports_check_mode=True)
    if module.check_mode:
        module.exit_json(changed=True)
    params = dict(access_token=module.params['token'], environment=module.params['environment'], revision=module.params['revision'])
    if module.params['user']:
        params['local_username'] = module.params['user']
    if module.params['rollbar_user']:
        params['rollbar_username'] = module.params['rollbar_user']
    if module.params['comment']:
        params['comment'] = module.params['comment']
    url = module.params.get('url')
    try:
        data = urlencode(params)
        (response, info) = fetch_url(module, url, data=data)
    except Exception as e:
        module.fail_json(msg=('Unable to notify Rollbar: %s' % to_native(e)), exception=traceback.format_exc())
    else:
        if (info['status'] == 200):
            module.exit_json(changed=True)
        else:
            module.fail_json(msg=('HTTP result code: %d connecting to %s' % (info['status'], url)))

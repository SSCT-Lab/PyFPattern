

def main():
    module = AnsibleModule(argument_spec=dict(check=dict(required=False), creator=dict(required=False), expire=dict(required=False), expire_on_resolve=dict(type='bool', required=False), reason=dict(required=False), state=dict(default='present', choices=['present', 'absent']), subscription=dict(required=True), url=dict(required=False, default='http://127.0.01:4567')), supports_check_mode=True)
    url = module.params['url']
    check = module.params['check']
    creator = module.params['creator']
    expire = module.params['expire']
    expire_on_resolve = module.params['expire_on_resolve']
    reason = module.params['reason']
    subscription = module.params['subscription']
    state = module.params['state']
    if (state == 'present'):
        (rc, out, changed) = create(module, url, check, creator, expire, expire_on_resolve, reason, subscription)
    if (state == 'absent'):
        (rc, out, changed) = clear(module, url, check, subscription)
    if (rc != 0):
        module.fail_json(msg='failed', result=out)
    module.exit_json(msg='success', result=out, changed=changed)

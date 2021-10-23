def main():
    rhsm = Rhsm(None)
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent']), username=dict(default=None, required=False), password=dict(default=None, required=False, no_log=True), server_hostname=dict(default=rhsm.config.get_option('server.hostname'), required=False), server_insecure=dict(default=rhsm.config.get_option('server.insecure'), required=False), rhsm_baseurl=dict(default=rhsm.config.get_option('rhsm.baseurl'), required=False), autosubscribe=dict(default=False, type='bool'), activationkey=dict(default=None, required=False), org_id=dict(default=None, required=False), environment=dict(default=None, required=False, type='str'), pool=dict(default='^$', required=False, type='str'), consumer_type=dict(default=None, required=False), consumer_name=dict(default=None, required=False), consumer_id=dict(default=None, required=False), force_register=dict(default=False, type='bool')), required_together=[['username', 'password'], ['activationkey', 'org_id']], mutually_exclusive=[['username', 'activationkey']])
    rhsm.module = module
    state = module.params['state']
    username = module.params['username']
    password = module.params['password']
    server_hostname = module.params['server_hostname']
    server_insecure = module.params['server_insecure']
    rhsm_baseurl = module.params['rhsm_baseurl']
    autosubscribe = (module.params['autosubscribe'] == True)
    activationkey = module.params['activationkey']
    org_id = module.params['org_id']
    environment = module.params['environment']
    pool = module.params['pool']
    consumer_type = module.params['consumer_type']
    consumer_name = module.params['consumer_name']
    consumer_id = module.params['consumer_id']
    force_register = module.params['force_register']
    global SUBMAN_CMD
    SUBMAN_CMD = module.get_bin_path('subscription-manager', True)
    if (state == 'present'):
        if (not (activationkey or org_id or username or password)):
            module.fail_json(msg=('Missing arguments, must supply an activationkey (%s) and Organization ID (%s) or username (%s) and password (%s)' % (activationkey, org_id, username, password)))
        if (rhsm.is_registered and (not force_register)):
            if (pool != '^$'):
                try:
                    result = rhsm.update_subscriptions(pool)
                except Exception:
                    e = get_exception()
                    module.fail_json(msg=("Failed to update subscriptions for '%s': %s" % (server_hostname, e)))
                else:
                    module.exit_json(**result)
            else:
                module.exit_json(changed=False, msg='System already registered.')
        else:
            try:
                rhsm.enable()
                rhsm.configure(**module.params)
                rhsm.register(username, password, autosubscribe, activationkey, org_id, consumer_type, consumer_name, consumer_id, force_register, environment)
                subscribed_pool_ids = rhsm.subscribe(pool)
            except Exception:
                e = get_exception()
                module.fail_json(msg=("Failed to register with '%s': %s" % (server_hostname, e)))
            else:
                module.exit_json(changed=True, msg=("System successfully registered to '%s'." % server_hostname), subscribed_pool_ids=subscribed_pool_ids)
    if (state == 'absent'):
        if (not rhsm.is_registered):
            module.exit_json(changed=False, msg='System already unregistered.')
        else:
            try:
                rhsm.unsubscribe()
                rhsm.unregister()
            except Exception:
                e = get_exception()
                module.fail_json(msg=('Failed to unregister: %s' % e))
            else:
                module.exit_json(changed=True, msg=('System successfully unregistered from %s.' % server_hostname))
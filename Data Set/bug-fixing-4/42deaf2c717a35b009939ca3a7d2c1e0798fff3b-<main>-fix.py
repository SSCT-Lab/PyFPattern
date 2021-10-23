def main():
    rhsm = Rhsm(None)
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent']), username=dict(default=None, required=False), password=dict(default=None, required=False, no_log=True), server_hostname=dict(default=rhsm.config.get_option('server.hostname'), required=False), server_insecure=dict(default=rhsm.config.get_option('server.insecure'), required=False), rhsm_baseurl=dict(default=rhsm.config.get_option('rhsm.baseurl'), required=False), auto_attach=dict(aliases=['autosubscribe'], default=False, type='bool'), activationkey=dict(default=None, required=False), org_id=dict(default=None, required=False), environment=dict(default=None, required=False, type='str'), pool=dict(default='^$', required=False, type='str'), pool_ids=dict(default=[], required=False, type='list'), consumer_type=dict(default=None, required=False), consumer_name=dict(default=None, required=False), consumer_id=dict(default=None, required=False), force_register=dict(default=False, type='bool'), server_proxy_hostname=dict(default=rhsm.config.get_option('server.proxy_hostname'), required=False), server_proxy_port=dict(default=rhsm.config.get_option('server.proxy_port'), required=False), server_proxy_user=dict(default=rhsm.config.get_option('server.proxy_user'), required=False), server_proxy_password=dict(default=rhsm.config.get_option('server.proxy_password'), required=False, no_log=True)), required_together=[['username', 'password'], ['server_proxy_hostname', 'server_proxy_port'], ['server_proxy_user', 'server_proxy_password']], mutually_exclusive=[['activationkey', 'username'], ['activationkey', 'consumer_id'], ['activationkey', 'environment'], ['activationkey', 'autosubscribe'], ['force', 'consumer_id'], ['pool', 'pool_ids']], required_if=[['state', 'present', ['username', 'activationkey'], True]])
    rhsm.module = module
    state = module.params['state']
    username = module.params['username']
    password = module.params['password']
    server_hostname = module.params['server_hostname']
    server_insecure = module.params['server_insecure']
    rhsm_baseurl = module.params['rhsm_baseurl']
    auto_attach = module.params['auto_attach']
    activationkey = module.params['activationkey']
    org_id = module.params['org_id']
    if (activationkey and (not org_id)):
        module.fail_json(msg='org_id is required when using activationkey')
    environment = module.params['environment']
    pool = module.params['pool']
    pool_ids = {
        
    }
    for value in module.params['pool_ids']:
        if isinstance(value, dict):
            if (len(value) != 1):
                module.fail_json(msg='Unable to parse pool_ids option.')
            (pool_id, quantity) = value.items()[0]
        else:
            (pool_id, quantity) = (value, 1)
        pool_ids[pool_id] = str(quantity)
    consumer_type = module.params['consumer_type']
    consumer_name = module.params['consumer_name']
    consumer_id = module.params['consumer_id']
    force_register = module.params['force_register']
    server_proxy_hostname = module.params['server_proxy_hostname']
    server_proxy_port = module.params['server_proxy_port']
    server_proxy_user = module.params['server_proxy_user']
    server_proxy_password = module.params['server_proxy_password']
    global SUBMAN_CMD
    SUBMAN_CMD = module.get_bin_path('subscription-manager', True)
    if (state == 'present'):
        if (rhsm.is_registered and (not force_register)):
            if ((pool != '^$') or pool_ids):
                try:
                    if pool_ids:
                        result = rhsm.update_subscriptions_by_pool_ids(pool_ids)
                    else:
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
                rhsm.register(username, password, auto_attach, activationkey, org_id, consumer_type, consumer_name, consumer_id, force_register, environment, rhsm_baseurl, server_insecure, server_hostname, server_proxy_hostname, server_proxy_port, server_proxy_user, server_proxy_password)
                if pool_ids:
                    subscribed_pool_ids = rhsm.subscribe_by_pool_ids(pool_ids)
                else:
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
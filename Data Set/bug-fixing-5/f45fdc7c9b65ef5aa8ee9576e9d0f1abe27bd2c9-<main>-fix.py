def main():
    argument_spec = postgres_common_argument_spec()
    argument_spec.update(name=dict(required=True), db=dict(type='str', aliases=['login_db']), state=dict(type='str', default='present', choices=['absent', 'present', 'refresh', 'stat']), publications=dict(type='list'), connparams=dict(type='dict'), cascade=dict(type='bool', default=False), owner=dict(type='str'), subsparams=dict(type='dict'), relinfo=dict(type='bool', default=False))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    db = module.params['db']
    name = module.params['name']
    state = module.params['state']
    publications = module.params['publications']
    cascade = module.params['cascade']
    owner = module.params['owner']
    subsparams = module.params['subsparams']
    connparams = module.params['connparams']
    relinfo = module.params['relinfo']
    if ((state == 'present') and cascade):
        module.warn('parameter "cascade" is ignored when state is not absent')
    if (state != 'present'):
        if owner:
            module.warn("parameter 'owner' is ignored when state is not 'present'")
        if publications:
            module.warn("parameter 'publications' is ignored when state is not 'present'")
        if connparams:
            module.warn("parameter 'connparams' is ignored when state is not 'present'")
        if subsparams:
            module.warn("parameter 'subsparams' is ignored when state is not 'present'")
    pg_conn_params = get_conn_params(module, module.params)
    db_connection = connect_to_db(module, pg_conn_params, autocommit=True)
    cursor = db_connection.cursor(cursor_factory=DictCursor)
    if (cursor.connection.server_version < SUPPORTED_PG_VERSION):
        module.fail_json(msg='PostgreSQL server version should be 10.0 or greater')
    changed = False
    initial_state = {
        
    }
    final_state = {
        
    }
    subscription = PgSubscription(module, cursor, name, db, relinfo)
    if subscription.exists:
        initial_state = deepcopy(subscription.attrs)
        final_state = deepcopy(initial_state)
    if (state == 'stat'):
        pass
    elif (state == 'present'):
        if (not subscription.exists):
            if subsparams:
                subsparams = convert_subscr_params(subsparams)
            if connparams:
                connparams = convert_conn_params(connparams)
            changed = subscription.create(connparams, publications, subsparams, check_mode=module.check_mode)
        else:
            changed = subscription.update(connparams, publications, subsparams, check_mode=module.check_mode)
        if (owner and (subscription.attrs['owner'] != owner)):
            changed = (subscription.set_owner(owner, check_mode=module.check_mode) or changed)
    elif (state == 'absent'):
        changed = subscription.drop(cascade, check_mode=module.check_mode)
    elif (state == 'refresh'):
        if (not subscription.exists):
            module.fail_json(msg=("Refresh failed: subscription '%s' does not exist" % name))
        changed = subscription.refresh(check_mode=module.check_mode)
    if (state != 'stat'):
        final_state = subscription.get_info()
    cursor.close()
    db_connection.close()
    module.exit_json(changed=changed, name=name, exists=subscription.exists, queries=subscription.executed_queries, initial_state=initial_state, final_state=final_state)
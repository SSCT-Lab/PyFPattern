

def main():
    module = AnsibleModule(argument_spec=dict(login_user=dict(default=None), login_password=dict(default=None, no_log=True), login_host=dict(default='localhost'), login_port=dict(default='27017'), login_database=dict(default=None), replica_set=dict(default=None), database=dict(required=True, aliases=['db']), name=dict(required=True, aliases=['user']), password=dict(aliases=['pass'], no_log=True), ssl=dict(default=False, type='bool'), roles=dict(default=None, type='list'), state=dict(default='present', choices=['absent', 'present']), update_password=dict(default='always', choices=['always', 'on_create']), ssl_cert_reqs=dict(default='CERT_REQUIRED', choices=['CERT_NONE', 'CERT_OPTIONAL', 'CERT_REQUIRED'])), supports_check_mode=True)
    if (not pymongo_found):
        module.fail_json(msg='the python pymongo module is required')
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_host = module.params['login_host']
    login_port = module.params['login_port']
    login_database = module.params['login_database']
    replica_set = module.params['replica_set']
    db_name = module.params['database']
    user = module.params['name']
    password = module.params['password']
    ssl = module.params['ssl']
    roles = (module.params['roles'] or [])
    state = module.params['state']
    update_password = module.params['update_password']
    try:
        connection_params = {
            'host': login_host,
            'port': int(login_port),
        }
        if replica_set:
            connection_params['replicaset'] = replica_set
        if ssl:
            connection_params['ssl'] = ssl
            connection_params['ssl_cert_reqs'] = getattr(ssl_lib, module.params['ssl_cert_reqs'])
        client = MongoClient(**connection_params)
        if (LooseVersion(PyMongoVersion) <= LooseVersion('3.5')):
            check_compatibility(module, client)
        if ((login_user is None) and (login_password is None)):
            mongocnf_creds = load_mongocnf()
            if (mongocnf_creds is not False):
                login_user = mongocnf_creds['user']
                login_password = mongocnf_creds['password']
        elif ((login_password is None) or (login_user is None)):
            module.fail_json(msg='when supplying login arguments, both login_user and login_password must be provided')
        if ((login_user is not None) and (login_password is not None)):
            client.admin.authenticate(login_user, login_password, source=login_database)
        elif (LooseVersion(PyMongoVersion) >= LooseVersion('3.0')):
            if (db_name != 'admin'):
                module.fail_json(msg='The localhost login exception only allows the first admin account to be created')
    except Exception as e:
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    if (state == 'present'):
        if ((password is None) and (update_password == 'always')):
            module.fail_json(msg='password parameter required when adding a user unless update_password is set to on_create')
        try:
            if (update_password != 'always'):
                uinfo = user_find(client, user, db_name)
                if uinfo:
                    password = None
                    if (not check_if_roles_changed(uinfo, roles, db_name)):
                        module.exit_json(changed=False, user=user)
            if module.check_mode:
                module.exit_json(changed=True, user=user)
            user_add(module, client, db_name, user, password, roles)
        except Exception as e:
            module.fail_json(msg=('Unable to add or update user: %s' % to_native(e)), exception=traceback.format_exc())
    elif (state == 'absent'):
        try:
            user_remove(module, client, db_name, user)
        except Exception as e:
            module.fail_json(msg=('Unable to remove user: %s' % to_native(e)), exception=traceback.format_exc())
    module.exit_json(changed=True, user=user)



def main():
    module = AnsibleModule(argument_spec=dict(login_user=dict(type='str'), login_password=dict(type='str', no_log=True), login_database=dict(type='str', default='admin'), login_host=dict(type='str', default='localhost'), login_port=dict(type='int', default=27017), replica_set=dict(type='str', default='rs0'), members=dict(type='list'), arbiter_at_index=dict(type='int'), validate=dict(type='bool', default=True), ssl=dict(type='bool', default=False), ssl_cert_reqs=dict(type='str', default='CERT_REQUIRED', choices=['CERT_NONE', 'CERT_OPTIONAL', 'CERT_REQUIRED']), protocol_version=dict(type='int', default=1, choices=[0, 1]), chaining_allowed=dict(type='bool', default=True), heartbeat_timeout_secs=dict(type='int', default=10), election_timeout_millis=dict(type='int', default=10000)), supports_check_mode=True)
    if (not HAS_PYMONGO):
        module.fail_json(msg='the python pymongo module is required')
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_database = module.params['login_database']
    login_host = module.params['login_host']
    login_port = module.params['login_port']
    replica_set = module.params['replica_set']
    members = module.params['members']
    arbiter_at_index = module.params['arbiter_at_index']
    validate = module.params['validate']
    ssl = module.params['ssl']
    protocol_version = module.params['protocol_version']
    chaining_allowed = module.params['chaining_allowed']
    heartbeat_timeout_secs = module.params['heartbeat_timeout_secs']
    election_timeout_millis = module.params['election_timeout_millis']
    if validate:
        if ((len(members) <= 2) or ((len(members) % 2) == 0)):
            module.fail_json(msg='MongoDB Replicaset validation failed. Invalid number of replicaset members.')
        if ((arbiter_at_index is not None) and ((len(members) - 1) > arbiter_at_index)):
            module.fail_json(msg='MongoDB Replicaset validation failed. Invalid arbiter index.')
    result = dict(changed=False, replica_set=replica_set)
    connection_params = dict(host=login_host, port=int(login_port))
    if ssl:
        connection_params['ssl'] = ssl
        connection_params['ssl_cert_reqs'] = getattr(ssl_lib, module.params['ssl_cert_reqs'])
    try:
        client = MongoClient(**connection_params)
    except Exception as e:
        module.fail_json(msg=('Unable to connect to database: %s' % to_native(e)))
    try:
        check_compatibility(module, client)
    except Exception as excep:
        if (('not authorized on' not in str(excep)) and ('there are no users authenticated' not in str(excep))):
            raise excep
        if ((login_user is None) or (login_password is None)):
            raise excep
        client.admin.authenticate(login_user, login_password, source=login_database)
        check_compatibility(module, client)
    if ((login_user is None) and (login_password is None)):
        mongocnf_creds = load_mongocnf()
        if (mongocnf_creds is not False):
            login_user = mongocnf_creds['user']
            login_password = mongocnf_creds['password']
    elif ((login_password is None) or (login_user is None)):
        module.fail_json(msg="When supplying login arguments, both 'login_user' and 'login_password' must be provided")
    try:
        client['admin'].command('listDatabases', 1.0)
    except Exception as excep:
        if (('not authorized on' in str(excep)) or ('command listDatabases requires authentication' in str(excep))):
            if ((login_user is not None) and (login_password is not None)):
                client.admin.authenticate(login_user, login_password, source=login_database)
            else:
                raise excep
        else:
            raise excep
    if (len(replica_set) == 0):
        module.fail_json(msg="Parameter 'replica_set' must not be an empty string")
    try:
        rs = replicaset_find(client)
    except Exception as e:
        module.fail_json(msg=('Unable to query replica_set info: %s' % to_native(e)))
    if (not rs):
        if (not module.check_mode):
            try:
                replicaset_add(module, client, replica_set, members, arbiter_at_index, protocol_version, chaining_allowed, heartbeat_timeout_secs, election_timeout_millis)
                result['changed'] = True
            except Exception as e:
                module.fail_json(msg=('Unable to create replica_set: %s' % to_native(e)))
    else:
        if (not module.check_mode):
            try:
                rs = replicaset_find(client)
            except Exception as e:
                module.fail_json(msg=('Unable to query replica_set info: %s' % to_native(e)))
            if ((rs is not None) and (rs != replica_set)):
                module.fail_json(msg="The replica_set name of '{0}' does not match the expected: '{1}'".format(rs, replica_set))
        result['changed'] = False
    module.exit_json(**result)

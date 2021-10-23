

def main():
    module = AnsibleModule(argument_spec=dict(login_user=dict(default=None), login_password=dict(default=None, no_log=True), login_database=dict(default='admin'), login_host=dict(default='localhost', required=False), login_port=dict(default=27017, type='int', required=False), ssl=dict(default=False, type='bool'), ssl_cert_reqs=dict(default='CERT_REQUIRED', choices=['CERT_NONE', 'CERT_OPTIONAL', 'CERT_REQUIRED']), shard=dict(default=None), state=dict(required=False, default='present', choices=['present', 'absent'])), supports_check_mode=True)
    if (not pymongo_found):
        module.fail_json(msg=missing_required_lib('pymongo'))
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_database = module.params['login_database']
    login_host = module.params['login_host']
    login_port = module.params['login_port']
    ssl = module.params['ssl']
    shard = module.params['shard']
    state = module.params['state']
    try:
        connection_params = {
            'host': login_host,
            'port': int(login_port),
        }
        if ssl:
            connection_params['ssl'] = ssl
            connection_params['ssl_cert_reqs'] = getattr(ssl_lib, module.params['ssl_cert_reqs'])
        client = MongoClient(**connection_params)
        try:
            check_compatibility(module, client)
        except Exception as excep:
            if (('not authorized on' in str(excep)) or ('there are no users authenticated' in str(excep))):
                if ((login_user is not None) and (login_password is not None)):
                    client.admin.authenticate(login_user, login_password, source=login_database)
                    check_compatibility(module, client)
                else:
                    raise excep
            else:
                raise excep
        if ((login_user is None) and (login_password is None)):
            mongocnf_creds = load_mongocnf()
            if (mongocnf_creds is not False):
                login_user = mongocnf_creds['user']
                login_password = mongocnf_creds['password']
        elif ((login_password is None) or (login_user is None)):
            module.fail_json(msg='when supplying login arguments, both login_user and login_password must be provided')
        try:
            client['admin'].command('listDatabases', 1.0)
        except Exception as excep:
            if ('not authorized on' in str(excep)):
                if ((login_user is not None) and (login_password is not None)):
                    client.admin.authenticate(login_user, login_password, source=login_database)
                else:
                    raise excep
            else:
                raise excep
    except Exception as e:
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    try:
        if (client['admin'].command('serverStatus')['process'] != 'mongos'):
            module.fail_json(msg='Process running on {0}:{1} is not a mongos'.format(login_host, login_port))
        shard_created = False
        if module.check_mode:
            if (state == 'present'):
                if (not shard_find(client, shard)):
                    changed = True
                else:
                    changed = False
            elif (state == 'absent'):
                if (not shard_find(client, shard)):
                    changed = False
                else:
                    changed = True
        elif (state == 'present'):
            if (not shard_find(client, shard)):
                shard_add(client, shard)
                changed = True
            else:
                changed = False
        elif (state == 'absent'):
            if shard_find(client, shard):
                shard_remove(client, shard)
                changed = True
            else:
                changed = False
    except Exception as e:
        action = 'add'
        if (state == 'absent'):
            action = 'remove'
        module.fail_json(msg=('Unable to {0} shard: %s'.format(action) % to_native(e)), exception=traceback.format_exc())
    module.exit_json(changed=changed, shard=shard)

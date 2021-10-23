

def main():
    module = AnsibleModule(argument_spec=dict(login_user=dict(default=None), login_password=dict(default=None, no_log=True), login_host=dict(default='localhost'), login_port=dict(default=27017, type='int'), login_database=dict(default=None), replica_set=dict(default=None), param=dict(default=None, required=True), value=dict(default=None, required=True), param_type=dict(default='str', choices=['str', 'int']), ssl=dict(default=False, type='bool')))
    if (not pymongo_found):
        module.fail_json(msg='the python pymongo module is required')
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_host = module.params['login_host']
    login_port = module.params['login_port']
    login_database = module.params['login_database']
    replica_set = module.params['replica_set']
    ssl = module.params['ssl']
    param = module.params['param']
    param_type = module.params['param_type']
    value = module.params['value']
    try:
        if (param_type == 'int'):
            value = int(value)
    except ValueError:
        e = get_exception()
        module.fail_json(msg=("value '%s' is not %s" % (value, param_type)))
    try:
        if replica_set:
            client = MongoClient(login_host, int(login_port), replicaset=replica_set, ssl=ssl)
        else:
            client = MongoClient(login_host, int(login_port), ssl=ssl)
        if ((login_user is None) and (login_password is None)):
            mongocnf_creds = load_mongocnf()
            if (mongocnf_creds is not False):
                login_user = mongocnf_creds['user']
                login_password = mongocnf_creds['password']
        elif ((login_password is None) or (login_user is None)):
            module.fail_json(msg='when supplying login arguments, both login_user and login_password must be provided')
        if ((login_user is not None) and (login_password is not None)):
            client.admin.authenticate(login_user, login_password, source=login_database)
    except ConnectionFailure:
        e = get_exception()
        module.fail_json(msg=('unable to connect to database: %s' % str(e)))
    db = client.admin
    try:
        after_value = db.command('setParameter', **{
            param: int(value),
        })
    except OperationFailure:
        e = get_exception()
        module.fail_json(msg=('unable to change parameter: %s' % str(e)))
    if ('was' not in after_value):
        module.exit_json(changed=True, msg='Unable to determine old value, assume it changed.')
    else:
        module.exit_json(changed=(value != after_value['was']), before=after_value['was'], after=value)

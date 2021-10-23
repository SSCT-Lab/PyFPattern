

def main():
    argument_spec = postgres_common_argument_spec()
    argument_spec.update(idxname=dict(type='str', required=True, aliases=['name']), db=dict(type='str'), ssl_mode=dict(type='str', default='prefer', choices=['allow', 'disable', 'prefer', 'require', 'verify-ca', 'verify-full']), ssl_rootcert=dict(type='str'), state=dict(type='str', default='present', choices=['absent', 'present']), concurrent=dict(type='bool', default=True), table=dict(type='str'), idxtype=dict(type='str', aliases=['type']), columns=dict(type='list'), cond=dict(type='str'), session_role=dict(type='str'), tablespace=dict(type='str'), storage_params=dict(type='list'), cascade=dict(type='bool', default=False), schema=dict(type='str'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    idxname = module.params['idxname']
    state = module.params['state']
    concurrent = module.params['concurrent']
    table = module.params['table']
    idxtype = module.params['idxtype']
    columns = module.params['columns']
    cond = module.params['cond']
    sslrootcert = module.params['ssl_rootcert']
    session_role = module.params['session_role']
    tablespace = module.params['tablespace']
    storage_params = module.params['storage_params']
    cascade = module.params['cascade']
    schema = module.params['schema']
    if (concurrent and (module.check_mode or cascade)):
        module.fail_json(msg='Cuncurrent mode and check mode/cascade are mutually exclusive')
    if (state == 'present'):
        if (not table):
            module.fail_json(msg='Table must be specified')
        if (not columns):
            module.fail_json(msg='At least one column must be specified')
    elif (table or columns or cond or idxtype or tablespace):
        module.fail_json(msg=('Index %s is going to be removed, so it does not make sense to pass a table name, columns, conditions, index type, or tablespace' % idxname))
    if (cascade and (state != 'absent')):
        module.fail_json(msg='cascade parameter used only with state=absent')
    if (not HAS_PSYCOPG2):
        module.fail_json(msg='the python psycopg2 module is required')
    params_map = {
        'login_host': 'host',
        'login_user': 'user',
        'login_password': 'password',
        'port': 'port',
        'db': 'database',
        'ssl_mode': 'sslmode',
        'ssl_rootcert': 'sslrootcert',
    }
    kw = dict(((params_map[k], v) for (k, v) in iteritems(module.params) if ((k in params_map) and (v != '') and (v is not None))))
    is_localhost = (('host' not in kw) or (kw['host'] is None) or (kw['host'] == 'localhost'))
    if (is_localhost and (module.params['login_unix_socket'] != '')):
        kw['host'] = module.params['login_unix_socket']
    if ((psycopg2.__version__ < '2.4.3') and (sslrootcert is not None)):
        module.fail_json(msg='psycopg2 must be at least 2.4.3 in order to user the ssl_rootcert parameter')
    if (module.check_mode and concurrent):
        module.fail_json(msg=('Cannot concurrently create or drop index %s inside the transaction block. The check is possible in not concurrent mode only' % idxname))
    try:
        db_connection = psycopg2.connect(**kw)
        if concurrent:
            if (psycopg2.__version__ >= '2.4.2'):
                db_connection.set_session(autocommit=True)
            else:
                db_connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except TypeError as e:
        if ('sslrootcert' in e.args[0]):
            module.fail_json(msg='Postgresql server must be at least version 8.4 to support sslrootcert')
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)))
    except Exception as e:
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)))
    if session_role:
        try:
            cursor.execute(('SET ROLE %s' % session_role))
        except Exception as e:
            module.fail_json(msg=('Could not switch role: %s' % to_native(e)))
    changed = False
    index = Index(module, cursor, schema, idxname)
    kw = index.get_info()
    kw['query'] = ''
    if (state == 'present'):
        if (idxtype and (idxtype.upper() not in VALID_IDX_TYPES)):
            module.fail_json(msg=("Index type '%s' of %s is not in valid types" % (idxtype, idxname)))
        columns = ','.join(columns)
        if storage_params:
            storage_params = ','.join(storage_params)
        changed = index.create(table, idxtype, columns, cond, tablespace, storage_params, concurrent)
        if changed:
            kw = index.get_info()
            kw['state'] = 'present'
            kw['query'] = index.executed_query
    else:
        changed = index.drop(schema, cascade, concurrent)
        if changed:
            kw['state'] = 'absent'
            kw['query'] = index.executed_query
    if ((not module.check_mode) and (not kw['valid']) and concurrent):
        db_connection.rollback()
        module.warn(msg=('Index %s is invalid! ROLLBACK' % idxname))
    if (not concurrent):
        if module.check_mode:
            db_connection.rollback()
        else:
            db_connection.commit()
    kw['changed'] = changed
    module.exit_json(**kw)

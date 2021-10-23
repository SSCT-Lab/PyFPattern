def main():
    argument_spec = pgutils.postgres_common_argument_spec()
    argument_spec.update(dict(idxname=dict(type='str', required=True, aliases=['idxname']), db=dict(type='str', default=''), ssl_mode=dict(type='str', default='prefer', choices=['allow', 'disable', 'prefer', 'require', 'verify-ca', 'verify-full']), ssl_rootcert=dict(type='str'), state=dict(type='str', default='present', choices=['absent', 'present']), concurrent=dict(type='bool', default=True), table=dict(type='str'), idxtype=dict(type='str'), columns=dict(type='str'), cond=dict(type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    idxname = module.params['idxname']
    state = module.params['state']
    concurrent = module.params['concurrent']
    table = module.params['table']
    idxtype = module.params['idxtype']
    columns = module.params['columns']
    cond = module.params['cond']
    sslrootcert = module.params['ssl_rootcert']
    if (state == 'present'):
        if (table is None):
            module.fail_json(msg='Table must be specified')
        if (columns is None):
            module.fail_json(msg='At least one column must be specified')
    else:
        if (table is not None):
            module.fail_json(msg=('Index %s is going to be removed, so it does not make sense to pass a table name' % idxname))
        if (columns is not None):
            module.fail_json(msg=('Index %s is going to be removed, so it does not make sense to pass column names' % idxname))
        if (cond is not None):
            module.fail_json(msg=('Index %s is going to be removed, so it does not make sense to pass any conditions' % idxname))
        if (idxtype is not None):
            module.fail_json(msg=('Index %s is going to be removed, so it does not make sense to pass an index type' % idxname))
    if (not postgresqldb_found):
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
    is_localhost = (('host' not in kw) or (kw['host'] == '') or (kw['host'] == 'localhost'))
    if (is_localhost and (module.params['login_unix_socket'] != '')):
        kw['host'] = module.params['login_unix_socket']
    if ((psycopg2.__version__ < '2.4.3') and (sslrootcert is not None)):
        module.fail_json(msg='psycopg2 must be at least 2.4.3 in order to user the ssl_rootcert parameter')
    if (module.check_mode and concurrent):
        module.fail_json(msg=('Cannot concurrently create or drop index %s inside the transaction block. The check is possible in not concurrent mode only' % idxname))
    try:
        db_connection = psycopg2.connect(**kw)
        if concurrent:
            db_connection.set_session(autocommit=True)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except TypeError as e:
        if ('sslrootcert' in e.args[0]):
            module.fail_json(msg='Postgresql server must be at least version 8.4 to support sslrootcert')
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    except Exception as e:
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    if ((state == 'present') and index_exists(cursor, idxname)):
        kw['changed'] = False
        del kw['login_password']
        module.exit_json(**kw)
    changed = False
    if (state == 'present'):
        if ((idxtype is not None) and (idxtype.upper() not in VALID_IDX_TYPES)):
            module.fail_json(msg=("Index type '%s' of %s is not in valid types" % (idxtype, idxname)))
        try:
            changed = index_create(cursor, module, idxname, table, idxtype, columns, cond, concurrent)
            kw['index_created'] = True
        except SQLParseError as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        except psycopg2.ProgrammingError as e:
            module.fail_json(msg=('Unable to create %s index with given requirement due to : %s' % (idxname, to_native(e))), exception=traceback.format_exc())
    else:
        try:
            changed = index_drop(cursor, module, idxname, concurrent)
            kw['index_dropped'] = True
        except SQLParseError as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        except psycopg2.ProgrammingError as e:
            module.fail_json(msg=('Unable to drop index %s due to : %s' % (idxname, to_native(e))), exception=traceback.format_exc())
    if (not concurrent):
        if changed:
            if module.check_mode:
                db_connection.rollback()
            else:
                db_connection.commit()
    if ((not module.check_mode) and (state != 'absent')):
        if (not index_valid(cursor, idxname, module)):
            kw['changed'] = changed
            module.fail_json(msg=('Index %s is invalid!' % idxname))
    kw['changed'] = changed
    del kw['login_password']
    module.exit_json(**kw)
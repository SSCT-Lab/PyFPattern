def main():
    module = AnsibleModule(argument_spec=dict(login_user=dict(default='postgres'), login_password=dict(default='', no_log=True), login_host=dict(default=''), login_unix_socket=dict(default=''), port=dict(default='5432'), schema=dict(required=True, aliases=['name']), owner=dict(default=''), database=dict(default='postgres'), cascade_drop=dict(type='bool', default=False), state=dict(default='present', choices=['absent', 'present']), ssl_mode=dict(default='prefer', choices=['disable', 'allow', 'prefer', 'require', 'verify-ca', 'verify-full']), ssl_rootcert=dict(default=None), session_role=dict()), supports_check_mode=True)
    if (not postgresqldb_found):
        module.fail_json(msg=missing_required_lib('psycopg2'), exception=PSYCOPG2_IMP_ERR)
    schema = module.params['schema']
    owner = module.params['owner']
    state = module.params['state']
    sslrootcert = module.params['ssl_rootcert']
    cascade_drop = module.params['cascade_drop']
    session_role = module.params['session_role']
    changed = False
    params_map = {
        'login_host': 'host',
        'login_user': 'user',
        'login_password': 'password',
        'port': 'port',
        'database': 'database',
        'ssl_mode': 'sslmode',
        'ssl_rootcert': 'sslrootcert',
    }
    kw = dict(((params_map[k], v) for (k, v) in iteritems(module.params) if ((k in params_map) and (v != '') and (v is not None))))
    is_localhost = (('host' not in kw) or (kw['host'] == '') or (kw['host'] == 'localhost'))
    if (is_localhost and (module.params['login_unix_socket'] != '')):
        kw['host'] = module.params['login_unix_socket']
    if ((psycopg2.__version__ < '2.4.3') and (sslrootcert is not None)):
        module.fail_json(msg='psycopg2 must be at least 2.4.3 in order to user the ssl_rootcert parameter')
    try:
        db_connection = psycopg2.connect(**kw)
        if (psycopg2.__version__ >= '2.4.2'):
            db_connection.autocommit = True
        else:
            db_connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except TypeError as e:
        if ('sslrootcert' in e.args[0]):
            module.fail_json(msg='Postgresql server must be at least version 8.4 to support sslrootcert')
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    except Exception as e:
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    if session_role:
        try:
            cursor.execute(('SET ROLE %s' % pg_quote_identifier(session_role, 'role')))
        except Exception as e:
            module.fail_json(msg=('Could not switch role: %s' % to_native(e)), exception=traceback.format_exc())
    try:
        if module.check_mode:
            if (state == 'absent'):
                changed = (not schema_exists(cursor, schema))
            elif (state == 'present'):
                changed = (not schema_matches(cursor, schema, owner))
            module.exit_json(changed=changed, schema=schema)
        if (state == 'absent'):
            try:
                changed = schema_delete(cursor, schema, cascade_drop)
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        elif (state == 'present'):
            try:
                changed = schema_create(cursor, schema, owner)
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    except NotSupportedError as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    except SystemExit:
        raise
    except Exception as e:
        module.fail_json(msg=('Database query failed: %s' % to_native(e)), exception=traceback.format_exc())
    module.exit_json(changed=changed, schema=schema)
def main():
    module = AnsibleModule(argument_spec=dict(login_user=dict(default='postgres'), login_password=dict(default='', no_log=True), login_host=dict(default=''), login_unix_socket=dict(default=''), port=dict(default='5432'), schema=dict(required=True, aliases=['name']), owner=dict(default=''), database=dict(default='postgres'), state=dict(default='present', choices=['absent', 'present'])), supports_check_mode=True)
    if (not postgresqldb_found):
        module.fail_json(msg='the python psycopg2 module is required')
    schema = module.params['schema']
    owner = module.params['owner']
    state = module.params['state']
    database = module.params['database']
    changed = False
    params_map = {
        'login_host': 'host',
        'login_user': 'user',
        'login_password': 'password',
        'port': 'port',
    }
    kw = dict(((params_map[k], v) for (k, v) in module.params.items() if ((k in params_map) and (v != ''))))
    is_localhost = (('host' not in kw) or (kw['host'] == '') or (kw['host'] == 'localhost'))
    if (is_localhost and (module.params['login_unix_socket'] != '')):
        kw['host'] = module.params['login_unix_socket']
    try:
        db_connection = psycopg2.connect(database=database, **kw)
        if (psycopg2.__version__ >= '2.4.2'):
            db_connection.autocommit = True
        else:
            db_connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except Exception:
        e = get_exception()
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    try:
        if module.check_mode:
            if (state == 'absent'):
                changed = (not schema_exists(cursor, schema))
            elif (state == 'present'):
                changed = (not schema_matches(cursor, schema, owner))
            module.exit_json(changed=changed, schema=schema)
        if (state == 'absent'):
            try:
                changed = schema_delete(cursor, schema)
            except SQLParseError:
                e = get_exception()
                module.fail_json(msg=str(e))
        elif (state == 'present'):
            try:
                changed = schema_create(cursor, schema, owner)
            except SQLParseError:
                e = get_exception()
                module.fail_json(msg=str(e))
    except NotSupportedError:
        e = get_exception()
        module.fail_json(msg=str(e))
    except SystemExit:
        raise
    except Exception:
        e = get_exception()
        module.fail_json(msg=('Database query failed: %s' % to_native(e)), exception=traceback.format_exc())
    module.exit_json(changed=changed, schema=schema)
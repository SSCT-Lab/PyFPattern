def main():
    argument_spec = pgutils.postgres_common_argument_spec()
    argument_spec.update(dict(db=dict(required=True, aliases=['name']), owner=dict(default=''), template=dict(default=''), encoding=dict(default=''), lc_collate=dict(default=''), lc_ctype=dict(default=''), state=dict(default='present', choices=['absent', 'present', 'dump', 'restore']), target=dict(default='', type='path'), target_opts=dict(default=''), maintenance_db=dict(default='postgres')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_PSYCOPG2):
        module.fail_json(msg='the python psycopg2 module is required')
    db = module.params['db']
    owner = module.params['owner']
    template = module.params['template']
    encoding = module.params['encoding']
    lc_collate = module.params['lc_collate']
    lc_ctype = module.params['lc_ctype']
    target = module.params['target']
    target_opts = module.params['target_opts']
    state = module.params['state']
    changed = False
    maintenance_db = module.params['maintenance_db']
    params_map = {
        'login_host': 'host',
        'login_user': 'user',
        'login_password': 'password',
        'port': 'port',
        'ssl_mode': 'sslmode',
        'ssl_rootcert': 'sslrootcert',
    }
    kw = dict(((params_map[k], v) for (k, v) in iteritems(module.params) if ((k in params_map) and (v != '') and (v is not None))))
    is_localhost = (('host' not in kw) or (kw['host'] == '') or (kw['host'] == 'localhost'))
    if (is_localhost and (module.params['login_unix_socket'] != '')):
        kw['host'] = module.params['login_unix_socket']
    if (target == ''):
        target = '{0}/{1}.sql'.format(os.getcwd(), db)
        target = os.path.expanduser(target)
    try:
        pgutils.ensure_libs(sslrootcert=module.params.get('ssl_rootcert'))
        db_connection = psycopg2.connect(database=maintenance_db, **kw)
        if (psycopg2.__version__ >= '2.4.2'):
            db_connection.autocommit = True
        else:
            db_connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except pgutils.LibraryError as e:
        module.fail_json(msg='unable to connect to database: {0}'.format(to_native(e)), exception=traceback.format_exc())
    except TypeError as e:
        if ('sslrootcert' in e.args[0]):
            module.fail_json(msg='Postgresql server must be at least version 8.4 to support sslrootcert. Exception: {0}'.format(to_native(e)), exception=traceback.format_exc())
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    except Exception as e:
        module.fail_json(msg=('unable to connect to database: %s' % to_native(e)), exception=traceback.format_exc())
    try:
        if module.check_mode:
            if (state == 'absent'):
                changed = db_exists(cursor, db)
            elif (state == 'present'):
                changed = (not db_matches(cursor, db, owner, template, encoding, lc_collate, lc_ctype))
            module.exit_json(changed=changed, db=db)
        if (state == 'absent'):
            try:
                changed = db_delete(cursor, db)
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        elif (state == 'present'):
            try:
                changed = db_create(cursor, db, owner, template, encoding, lc_collate, lc_ctype)
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        elif (state in ('dump', 'restore')):
            if ((not db_exists(cursor, db)) and (state == 'dump')):
                module.fail_json(msg='database "{db}" does not exist'.format(db=db))
            method = (((state == 'dump') and db_dump) or db_restore)
            try:
                (rc, stdout, stderr, cmd) = method(module, target, target_opts, db, **kw)
                if (rc != 0):
                    module.fail_json(msg=stderr, stdout=stdout, rc=rc, cmd=cmd)
                else:
                    module.exit_json(changed=True, msg=stdout, stderr=stderr, rc=rc, cmd=cmd)
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    except NotSupportedError as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    except SystemExit:
        raise
    except Exception as e:
        module.fail_json(msg=('Database query failed: %s' % to_native(e)), exception=traceback.format_exc())
    module.exit_json(changed=changed, db=db)
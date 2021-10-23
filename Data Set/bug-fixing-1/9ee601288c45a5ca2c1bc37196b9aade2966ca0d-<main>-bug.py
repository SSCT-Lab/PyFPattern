

def main():
    argument_spec = postgres_common_argument_spec()
    argument_spec.update(user=dict(type='str', required=True, aliases=['name']), password=dict(type='str', default=None, no_log=True), state=dict(type='str', default='present', choices=['absent', 'present']), priv=dict(type='str', default=None), db=dict(type='str', default='', aliases=['login_db']), fail_on_user=dict(type='bool', default='yes', aliases=['fail_on_role']), role_attr_flags=dict(type='str', default=''), encrypted=dict(type='bool', default='yes'), no_password_changes=dict(type='bool', default='no'), expires=dict(type='str', default=None), conn_limit=dict(type='int', default=None), session_role=dict(type='str'), groups=dict(type='list'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    user = module.params['user']
    password = module.params['password']
    state = module.params['state']
    fail_on_user = module.params['fail_on_user']
    if ((module.params['db'] == '') and (module.params['priv'] is not None)):
        module.fail_json(msg='privileges require a database to be specified')
    privs = parse_privs(module.params['priv'], module.params['db'])
    no_password_changes = module.params['no_password_changes']
    if module.params['encrypted']:
        encrypted = 'ENCRYPTED'
    else:
        encrypted = 'UNENCRYPTED'
    expires = module.params['expires']
    conn_limit = module.params['conn_limit']
    role_attr_flags = module.params['role_attr_flags']
    groups = module.params['groups']
    if groups:
        groups = [e.strip() for e in groups]
    conn_params = get_conn_params(module, module.params, warn_db_default=False)
    db_connection = connect_to_db(module, conn_params)
    cursor = db_connection.cursor(cursor_factory=DictCursor)
    try:
        role_attr_flags = parse_role_attrs(cursor, role_attr_flags)
    except InvalidFlagsError as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    kw = dict(user=user)
    changed = False
    user_removed = False
    if (state == 'present'):
        if user_exists(cursor, user):
            try:
                changed = user_alter(db_connection, module, user, password, role_attr_flags, encrypted, expires, no_password_changes, conn_limit)
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        else:
            try:
                changed = user_add(cursor, user, password, role_attr_flags, encrypted, expires, conn_limit)
            except psycopg2.ProgrammingError as e:
                module.fail_json(msg=('Unable to add user with given requirement due to : %s' % to_native(e)), exception=traceback.format_exc())
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        try:
            changed = (grant_privileges(cursor, user, privs) or changed)
        except SQLParseError as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        if groups:
            target_roles = []
            target_roles.append(user)
            pg_membership = PgMembership(module, cursor, groups, target_roles)
            changed = pg_membership.grant()
            executed_queries.extend(pg_membership.executed_queries)
    elif user_exists(cursor, user):
        if module.check_mode:
            changed = True
            kw['user_removed'] = True
        else:
            try:
                changed = revoke_privileges(cursor, user, privs)
                user_removed = user_delete(cursor, user)
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
            changed = (changed or user_removed)
            if (fail_on_user and (not user_removed)):
                msg = 'Unable to remove user'
                module.fail_json(msg=msg)
            kw['user_removed'] = user_removed
    if changed:
        if module.check_mode:
            db_connection.rollback()
        else:
            db_connection.commit()
    kw['changed'] = changed
    kw['queries'] = executed_queries
    module.exit_json(**kw)

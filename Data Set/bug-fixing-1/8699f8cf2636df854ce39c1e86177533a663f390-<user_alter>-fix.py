

def user_alter(db_connection, module, user, password, role_attr_flags, encrypted, expires, no_password_changes, conn_limit):
    'Change user password and/or attributes. Return True if changed, False otherwise.'
    changed = False
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if (user == 'PUBLIC'):
        if (password is not None):
            module.fail_json(msg='cannot change the password for PUBLIC user')
        elif (role_attr_flags != ''):
            module.fail_json(msg='cannot change the role_attr_flags for PUBLIC user')
        else:
            return False
    if ((not no_password_changes) and ((password is not None) or (role_attr_flags != '') or (expires is not None) or (conn_limit is not None))):
        try:
            select = 'SELECT * FROM pg_authid where rolname=%(user)s'
            cursor.execute(select, {
                'user': user,
            })
            current_role_attrs = cursor.fetchone()
        except psycopg2.ProgrammingError:
            current_role_attrs = None
            db_connection.rollback()
        pwchanging = user_should_we_change_password(current_role_attrs, user, password, encrypted)
        if (current_role_attrs is None):
            try:
                select = 'SELECT * FROM pg_roles where rolname=%(user)s'
                cursor.execute(select, {
                    'user': user,
                })
                current_role_attrs = cursor.fetchone()
            except psycopg2.ProgrammingError as e:
                db_connection.rollback()
                module.fail_json(msg=('Failed to get role details for current user %s: %s' % (user, e)))
        role_attr_flags_changing = False
        if role_attr_flags:
            role_attr_flags_dict = {
                
            }
            for r in role_attr_flags.split(' '):
                if r.startswith('NO'):
                    role_attr_flags_dict[r.replace('NO', '', 1)] = False
                else:
                    role_attr_flags_dict[r] = True
            for (role_attr_name, role_attr_value) in role_attr_flags_dict.items():
                if (current_role_attrs[PRIV_TO_AUTHID_COLUMN[role_attr_name]] != role_attr_value):
                    role_attr_flags_changing = True
        if (expires is not None):
            cursor.execute('SELECT %s::timestamptz;', (expires,))
            expires_with_tz = cursor.fetchone()[0]
            expires_changing = (expires_with_tz != current_role_attrs.get('rolvaliduntil'))
        else:
            expires_changing = False
        conn_limit_changing = ((conn_limit is not None) and (conn_limit != current_role_attrs['rolconnlimit']))
        if ((not pwchanging) and (not role_attr_flags_changing) and (not expires_changing) and (not conn_limit_changing)):
            return False
        alter = [('ALTER USER %(user)s' % {
            'user': pg_quote_identifier(user, 'role'),
        })]
        if pwchanging:
            alter.append(('WITH %(crypt)s' % {
                'crypt': encrypted,
            }))
            alter.append('PASSWORD %(password)s')
            alter.append(role_attr_flags)
        elif role_attr_flags:
            alter.append(('WITH %s' % role_attr_flags))
        if (expires is not None):
            alter.append('VALID UNTIL %(expires)s')
        if (conn_limit is not None):
            alter.append(('CONNECTION LIMIT %(conn_limit)s' % {
                'conn_limit': conn_limit,
            }))
        query_password_data = dict(password=password, expires=expires)
        try:
            cursor.execute(' '.join(alter), query_password_data)
            changed = True
        except psycopg2.InternalError as e:
            if (e.pgcode == '25006'):
                changed = False
                module.fail_json(msg=e.pgerror, exception=traceback.format_exc())
                return changed
            else:
                raise psycopg2.InternalError(e)
    elif (no_password_changes and (role_attr_flags != '')):
        select = 'SELECT * FROM pg_roles where rolname=%(user)s'
        cursor.execute(select, {
            'user': user,
        })
        current_role_attrs = cursor.fetchone()
        role_attr_flags_changing = False
        if role_attr_flags:
            role_attr_flags_dict = {
                
            }
            for r in role_attr_flags.split(' '):
                if r.startswith('NO'):
                    role_attr_flags_dict[r.replace('NO', '', 1)] = False
                else:
                    role_attr_flags_dict[r] = True
            for (role_attr_name, role_attr_value) in role_attr_flags_dict.items():
                if (current_role_attrs[PRIV_TO_AUTHID_COLUMN[role_attr_name]] != role_attr_value):
                    role_attr_flags_changing = True
        if (not role_attr_flags_changing):
            return False
        alter = [('ALTER USER %(user)s' % {
            'user': pg_quote_identifier(user, 'role'),
        })]
        if role_attr_flags:
            alter.append(('WITH %s' % role_attr_flags))
        try:
            cursor.execute(' '.join(alter))
        except psycopg2.InternalError as e:
            if (e.pgcode == '25006'):
                changed = False
                module.fail_json(msg=e.pgerror, exception=traceback.format_exc())
                return changed
            else:
                raise psycopg2.InternalError(e)
        cursor.execute(select, {
            'user': user,
        })
        new_role_attrs = cursor.fetchone()
        changed = (current_role_attrs != new_role_attrs)
    return changed

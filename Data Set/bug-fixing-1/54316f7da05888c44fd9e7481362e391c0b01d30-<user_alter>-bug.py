

def user_alter(cursor, module, user, password, role_attr_flags, encrypted, expires, no_password_changes):
    'Change user password and/or attributes. Return True if changed, False otherwise.'
    changed = False
    if (user == 'PUBLIC'):
        if (password is not None):
            module.fail_json(msg='cannot change the password for PUBLIC user')
        elif (role_attr_flags != ''):
            module.fail_json(msg='cannot change the role_attr_flags for PUBLIC user')
        else:
            return False
    if ((not no_password_changes) and ((password is not None) or (role_attr_flags != ''))):
        query_password_data = dict(password=password, expires=expires)
        select = 'SELECT * FROM pg_authid where rolname=%(user)s'
        cursor.execute(select, {
            'user': user,
        })
        current_role_attrs = cursor.fetchone()
        pwchanging = False
        if (password is not None):
            if encrypted:
                if password.startswith('md5'):
                    if (password != current_role_attrs['rolpassword']):
                        pwchanging = True
                else:
                    try:
                        from passlib.hash import postgres_md5 as pm
                        if (pm.encrypt(password, user) != current_role_attrs['rolpassword']):
                            pwchanging = True
                    except ImportError:
                        pwchanging = True
            elif (password != current_role_attrs['rolpassword']):
                pwchanging = True
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
        expires_changing = ((expires is not None) and (expires == current_roles_attrs['rol_valid_until']))
        if ((not pwchanging) and (not role_attr_flags_changing) and (not expires_changing)):
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
        try:
            cursor.execute(' '.join(alter), query_password_data)
        except psycopg2.InternalError:
            e = get_exception()
            if (e.pgcode == '25006'):
                changed = False
                module.fail_json(msg=e.pgerror)
                return changed
            else:
                raise psycopg2.InternalError(e)
        cursor.execute(select, {
            'user': user,
        })
        new_role_attrs = cursor.fetchone()
        for i in range(len(current_role_attrs)):
            if (current_role_attrs[i] != new_role_attrs[i]):
                changed = True
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
        except psycopg2.InternalError:
            e = get_exception()
            if (e.pgcode == '25006'):
                changed = False
                module.fail_json(msg=e.pgerror)
                return changed
            else:
                raise psycopg2.InternalError(e)
        cursor.execute(select, {
            'user': user,
        })
        new_role_attrs = cursor.fetchone()
        for i in range(len(current_role_attrs)):
            if (current_role_attrs[i] != new_role_attrs[i]):
                changed = True
    return changed

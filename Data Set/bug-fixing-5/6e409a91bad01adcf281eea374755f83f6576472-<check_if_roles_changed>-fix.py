def check_if_roles_changed(uinfo, roles, db_name):

    def make_sure_roles_are_a_list_of_dict(roles, db_name):
        output = list()
        for role in roles:
            if isinstance(role, (binary_type, text_type)):
                new_role = {
                    'role': role,
                    'db': db_name,
                }
                output.append(new_role)
            else:
                output.append(role)
        return output
    roles_as_list_of_dict = make_sure_roles_are_a_list_of_dict(roles, db_name)
    uinfo_roles = uinfo.get('roles', [])
    if (sorted(roles_as_list_of_dict, key=itemgetter('db')) == sorted(uinfo_roles, key=itemgetter('db'))):
        return False
    return True
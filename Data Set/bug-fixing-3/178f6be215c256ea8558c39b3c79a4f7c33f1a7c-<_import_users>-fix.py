def _import_users(users_list):
    appbuilder = cached_appbuilder()
    users_created = []
    users_updated = []
    for user in users_list:
        roles = []
        for rolename in user['roles']:
            role = appbuilder.sm.find_role(rolename)
            if (not role):
                valid_roles = appbuilder.sm.get_all_roles()
                print("Error: '{}' is not a valid role. Valid roles are: {}".format(rolename, valid_roles))
                exit(1)
            else:
                roles.append(role)
        required_fields = ['username', 'firstname', 'lastname', 'email', 'roles']
        for field in required_fields:
            if (not user.get(field)):
                print("Error: '{}' is a required field, but was not specified".format(field))
                exit(1)
        existing_user = appbuilder.sm.find_user(email=user['email'])
        if existing_user:
            print("Found existing user with email '{}'".format(user['email']))
            existing_user.roles = roles
            existing_user.first_name = user['firstname']
            existing_user.last_name = user['lastname']
            if (existing_user.username != user['username']):
                print("Error: Changing the username is not allowed - please delete and recreate the user with email '{}'".format(user['email']))
                exit(1)
            appbuilder.sm.update_user(existing_user)
            users_updated.append(user['email'])
        else:
            print("Creating new user with email '{}'".format(user['email']))
            appbuilder.sm.add_user(username=user['username'], first_name=user['firstname'], last_name=user['lastname'], email=user['email'], role=roles[0])
            if (len(roles) > 1):
                new_user = appbuilder.sm.find_user(email=user['email'])
                new_user.roles = roles
                appbuilder.sm.update_user(new_user)
            users_created.append(user['email'])
    return (users_created, users_updated)
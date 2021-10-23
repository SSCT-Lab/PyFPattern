@cli_utils.action_logging
def users_manage_role(args, remove=False):
    if ((not args.username) and (not args.email)):
        raise SystemExit('Missing args: must supply one of --username or --email')
    if (args.username and args.email):
        raise SystemExit('Conflicting args: must supply either --username or --email, but not both')
    appbuilder = cached_appbuilder()
    user = (appbuilder.sm.find_user(username=args.username) or appbuilder.sm.find_user(email=args.email))
    if (not user):
        raise SystemExit('User "{}" does not exist'.format((args.username or args.email)))
    role = appbuilder.sm.find_role(args.role)
    if (not role):
        raise SystemExit('"{}" is not a valid role.'.format(args.role))
    if remove:
        if (role in user.roles):
            user.roles = [r for r in user.roles if (r != role)]
            appbuilder.sm.update_user(user)
            print('User "{}" removed from role "{}".'.format(user, args.role))
        else:
            raise SystemExit('User "{}" is not a member of role "{}".'.format(user, args.role))
    elif (role in user.roles):
        raise SystemExit('User "{}" is already a member of role "{}".'.format(user, args.role))
    else:
        user.roles.append(role)
        appbuilder.sm.update_user(user)
        print('User "{}" added to role "{}".'.format(user, args.role))
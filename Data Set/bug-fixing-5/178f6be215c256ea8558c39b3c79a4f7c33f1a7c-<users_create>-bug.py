@cli_utils.action_logging
def users_create(args):
    appbuilder = cached_appbuilder()
    role = appbuilder.sm.find_role(args.role)
    if (not role):
        raise SystemExit('{} is not a valid role.'.format(args.role))
    if args.use_random_password:
        password = ''.join((random.choice(string.printable) for _ in range(16)))
    elif args.password:
        password = args.password
    else:
        password = getpass.getpass('Password:')
        password_confirmation = getpass.getpass('Repeat for confirmation:')
        if (password != password_confirmation):
            raise SystemExit('Passwords did not match!')
    if appbuilder.sm.find_user(args.username):
        print('{} already exist in the db'.format(args.username))
        return
    user = appbuilder.sm.add_user(args.username, args.firstname, args.lastname, args.email, role, password)
    if user:
        print('{} user {} created.'.format(args.role, args.username))
    else:
        raise SystemExit('Failed to create user.')
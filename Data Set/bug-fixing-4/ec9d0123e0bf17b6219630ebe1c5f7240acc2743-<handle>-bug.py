def handle(self, *args, **options):
    username = options[self.UserModel.USERNAME_FIELD]
    database = options['database']
    password = None
    user_data = {
        
    }
    fake_user_data = {
        
    }
    verbose_field_name = self.username_field.verbose_name
    try:
        if options['interactive']:
            if (hasattr(self.stdin, 'isatty') and (not self.stdin.isatty())):
                raise NotRunningInTTYException
            default_username = get_default_username()
            if username:
                error_msg = self._validate_username(username, verbose_field_name, database)
                if error_msg:
                    self.stderr.write(error_msg)
                    username = None
            elif (username == ''):
                raise CommandError(('%s cannot be blank.' % capfirst(verbose_field_name)))
            while (username is None):
                input_msg = capfirst(verbose_field_name)
                if default_username:
                    input_msg += (" (leave blank to use '%s')" % default_username)
                username_rel = self.username_field.remote_field
                input_msg = ('%s%s: ' % (input_msg, ((' (%s.%s)' % (username_rel.model._meta.object_name, username_rel.field_name)) if username_rel else '')))
                username = self.get_input_data(self.username_field, input_msg, default_username)
                if username:
                    error_msg = self._validate_username(username, verbose_field_name, database)
                    if error_msg:
                        self.stderr.write(error_msg)
                        username = None
                        continue
        elif (username is None):
            raise CommandError(('You must use --%s with --noinput.' % self.UserModel.USERNAME_FIELD))
        else:
            error_msg = self._validate_username(username, verbose_field_name, database)
            if error_msg:
                raise CommandError(error_msg)
        user_data[self.UserModel.USERNAME_FIELD] = username
        fake_user_data[self.UserModel.USERNAME_FIELD] = (self.username_field.remote_field.model(username) if self.username_field.remote_field else username)
        for field_name in self.UserModel.REQUIRED_FIELDS:
            if (not options['interactive']):
                if options[field_name]:
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = field.clean(options[field_name], None)
                else:
                    raise CommandError(('You must use --%s with --noinput.' % field_name))
            else:
                field = self.UserModel._meta.get_field(field_name)
                user_data[field_name] = options[field_name]
                while (user_data[field_name] is None):
                    message = ('%s%s: ' % (capfirst(field.verbose_name), ((' (%s.%s)' % (field.remote_field.model._meta.object_name, field.remote_field.field_name)) if field.remote_field else '')))
                    input_value = self.get_input_data(field, message)
                    user_data[field_name] = input_value
                    fake_user_data[field_name] = input_value
                    if field.remote_field:
                        fake_user_data[field_name] = field.remote_field.model(input_value)
        if options['interactive']:
            while (password is None):
                password = getpass.getpass()
                password2 = getpass.getpass('Password (again): ')
                if (password != password2):
                    self.stderr.write("Error: Your passwords didn't match.")
                    password = None
                    continue
                if (password.strip() == ''):
                    self.stderr.write("Error: Blank passwords aren't allowed.")
                    password = None
                    continue
                try:
                    validate_password(password2, self.UserModel(**fake_user_data))
                except exceptions.ValidationError as err:
                    self.stderr.write('\n'.join(err.messages))
                    response = input('Bypass password validation and create user anyway? [y/N]: ')
                    if (response.lower() != 'y'):
                        password = None
        user_data['password'] = password
        self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)
        if (options['verbosity'] >= 1):
            self.stdout.write('Superuser created successfully.')
    except KeyboardInterrupt:
        self.stderr.write('\nOperation cancelled.')
        sys.exit(1)
    except exceptions.ValidationError as e:
        raise CommandError('; '.join(e.messages))
    except NotRunningInTTYException:
        self.stdout.write('Superuser creation skipped due to not running in a TTY. You can run `manage.py createsuperuser` in your project to create one manually.')
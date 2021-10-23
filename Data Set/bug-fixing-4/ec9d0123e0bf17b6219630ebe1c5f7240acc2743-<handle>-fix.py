def handle(self, *args, **options):
    username = options[self.UserModel.USERNAME_FIELD]
    database = options['database']
    password = None
    user_data = {
        
    }
    verbose_field_name = self.username_field.verbose_name
    try:
        if options['interactive']:
            fake_user_data = {
                
            }
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
                message = self._get_input_message(self.username_field, default_username)
                username = self.get_input_data(self.username_field, message, default_username)
                if username:
                    error_msg = self._validate_username(username, verbose_field_name, database)
                    if error_msg:
                        self.stderr.write(error_msg)
                        username = None
                        continue
            user_data[self.UserModel.USERNAME_FIELD] = username
            fake_user_data[self.UserModel.USERNAME_FIELD] = (self.username_field.remote_field.model(username) if self.username_field.remote_field else username)
            for field_name in self.UserModel.REQUIRED_FIELDS:
                field = self.UserModel._meta.get_field(field_name)
                user_data[field_name] = options[field_name]
                while (user_data[field_name] is None):
                    message = self._get_input_message(field)
                    input_value = self.get_input_data(field, message)
                    user_data[field_name] = input_value
                    fake_user_data[field_name] = input_value
                    if field.remote_field:
                        fake_user_data[field_name] = field.remote_field.model(input_value)
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
        else:
            if (username is None):
                raise CommandError(('You must use --%s with --noinput.' % self.UserModel.USERNAME_FIELD))
            else:
                error_msg = self._validate_username(username, verbose_field_name, database)
                if error_msg:
                    raise CommandError(error_msg)
            user_data[self.UserModel.USERNAME_FIELD] = username
            for field_name in self.UserModel.REQUIRED_FIELDS:
                if options[field_name]:
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = field.clean(options[field_name], None)
                else:
                    raise CommandError(('You must use --%s with --noinput.' % field_name))
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
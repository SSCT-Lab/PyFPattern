def call_command(command_name, *args, **options):
    "\n    Call the given command, with the given options and args/kwargs.\n\n    This is the primary API you should use for calling specific commands.\n\n    `name` may be a string or a command object. Using a string is preferred\n    unless the command object is required for further processing or testing.\n\n    Some examples:\n        call_command('migrate')\n        call_command('shell', plain=True)\n        call_command('sqlmigrate', 'myapp')\n\n        from django.core.management.commands import flush\n        cmd = flush.Command()\n        call_command(cmd, verbosity=0, interactive=False)\n        # Do something with cmd ...\n    "
    if isinstance(command_name, BaseCommand):
        command = command_name
        command_name = command.__class__.__module__.split('.')[(- 1)]
    else:
        try:
            app_name = get_commands()[command_name]
        except KeyError:
            raise CommandError(('Unknown command: %r' % command_name))
        if isinstance(app_name, BaseCommand):
            command = app_name
        else:
            command = load_command_class(app_name, command_name)
    parser = command.create_parser('', command_name)
    opt_mapping = {min(s_opt.option_strings).lstrip('-').replace('-', '_'): s_opt.dest for s_opt in parser._actions if s_opt.option_strings}
    arg_options = {opt_mapping.get(key, key): value for (key, value) in options.items()}
    defaults = parser.parse_args(args=[force_text(a) for a in args])
    defaults = dict(defaults._get_kwargs(), **arg_options)
    stealth_options = set((command.base_stealth_options + command.stealth_options))
    dest_parameters = {action.dest for action in parser._actions}
    valid_options = (dest_parameters | stealth_options).union(opt_mapping)
    unknown_options = (set(options) - valid_options)
    if unknown_options:
        raise TypeError(('Unknown option(s) for %s command: %s. Valid options are: %s.' % (command_name, ', '.join(sorted(unknown_options)), ', '.join(sorted(valid_options)))))
    args = defaults.pop('args', ())
    if ('skip_checks' not in options):
        defaults['skip_checks'] = True
    return command.execute(*args, **defaults)
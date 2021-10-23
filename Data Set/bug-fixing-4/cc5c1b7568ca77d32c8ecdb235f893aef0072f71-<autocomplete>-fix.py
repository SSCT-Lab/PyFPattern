def autocomplete(self):
    "\n        Output completion suggestions for BASH.\n\n        The output of this function is passed to BASH's `COMREPLY` variable and\n        treated as completion suggestions. `COMREPLY` expects a space\n        separated string as the result.\n\n        The `COMP_WORDS` and `COMP_CWORD` BASH environment variables are used\n        to get information about the cli input. Please refer to the BASH\n        man-page for more information about this variables.\n\n        Subcommand options are saved as pairs. A pair consists of\n        the long option string (e.g. '--exclude') and a boolean\n        value indicating if the option requires arguments. When printing to\n        stdout, an equal sign is appended to options which require arguments.\n\n        Note: If debugging this function, it is recommended to write the debug\n        output in a separate file. Otherwise the debug output will be treated\n        and formatted as potential completion suggestions.\n        "
    if ('DJANGO_AUTO_COMPLETE' not in os.environ):
        return
    cwords = os.environ['COMP_WORDS'].split()[1:]
    cword = int(os.environ['COMP_CWORD'])
    try:
        curr = cwords[(cword - 1)]
    except IndexError:
        curr = ''
    subcommands = (list(get_commands()) + ['help'])
    options = [('--help', False)]
    if (cword == 1):
        print(' '.join(sorted(filter((lambda x: x.startswith(curr)), subcommands))))
    elif ((cwords[0] in subcommands) and (cwords[0] != 'help')):
        subcommand_cls = self.fetch_command(cwords[0])
        if (cwords[0] in ('dumpdata', 'sqlmigrate', 'sqlsequencereset', 'test')):
            try:
                app_configs = apps.get_app_configs()
                options.extend(((app_config.label, 0) for app_config in app_configs))
            except ImportError:
                pass
        parser = subcommand_cls.create_parser('', cwords[0])
        options.extend(((min(s_opt.option_strings), (s_opt.nargs != 0)) for s_opt in parser._actions if s_opt.option_strings))
        prev_opts = {x.split('=')[0] for x in cwords[1:(cword - 1)]}
        options = (opt for opt in options if (opt[0] not in prev_opts))
        options = sorted(((k, v) for (k, v) in options if k.startswith(curr)))
        for (opt_label, require_arg) in options:
            if require_arg:
                opt_label += '='
            print(opt_label)
    sys.exit(0)
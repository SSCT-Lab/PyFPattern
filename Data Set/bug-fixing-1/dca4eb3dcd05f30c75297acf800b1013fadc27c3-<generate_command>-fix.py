

def generate_command(args, path, options, exclude, require):
    '\n    :type args: EnvironmentConfig\n    :type path: str\n    :type options: dict[str, int]\n    :type exclude: list[str]\n    :type require: list[str]\n    :rtype: list[str]\n    '
    options['--color'] = 1
    cmd = [path]
    cmd = (['/usr/bin/env', 'LC_ALL=en_US.UTF-8'] + cmd)
    cmd += list(filter_options(args, sys.argv[1:], options, exclude, require))
    cmd += ['--color', ('yes' if args.color else 'no')]
    if args.requirements:
        cmd += ['--requirements']
    if isinstance(args, ShellConfig):
        cmd = create_shell_command(cmd)
    elif isinstance(args, SanityConfig):
        if args.base_branch:
            cmd += ['--base-branch', args.base_branch]
    return cmd

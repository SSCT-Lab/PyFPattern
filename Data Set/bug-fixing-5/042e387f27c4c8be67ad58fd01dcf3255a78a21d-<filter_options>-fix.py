def filter_options(args, argv, options, exclude, require):
    '\n    :type args: EnvironmentConfig\n    :type argv: list[str]\n    :type options: dict[str, int]\n    :type exclude: list[str]\n    :type require: list[str]\n    :rtype: collections.Iterable[str]\n    '
    options = options.copy()
    options['--requirements'] = 0
    if isinstance(args, TestConfig):
        options.update({
            '--changed': 0,
            '--tracked': 0,
            '--untracked': 0,
            '--ignore-committed': 0,
            '--ignore-staged': 0,
            '--ignore-unstaged': 0,
            '--changed-from': 1,
            '--changed-path': 1,
            '--metadata': 1,
        })
    elif isinstance(args, SanityConfig):
        options.update({
            '--base-branch': 1,
        })
    remaining = 0
    for arg in argv:
        if ((not arg.startswith('-')) and remaining):
            remaining -= 1
            continue
        remaining = 0
        parts = arg.split('=', 1)
        key = parts[0]
        if (key in options):
            remaining = ((options[key] - len(parts)) + 1)
            continue
        (yield arg)
    for target in exclude:
        (yield '--exclude')
        (yield target)
    for target in require:
        (yield '--require')
        (yield target)
    if isinstance(args, TestConfig):
        if args.metadata_path:
            (yield '--metadata')
            (yield args.metadata_path)
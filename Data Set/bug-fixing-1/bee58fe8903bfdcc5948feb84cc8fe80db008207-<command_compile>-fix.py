

def command_compile(args):
    '\n    :type args: CompileConfig\n    '
    changes = get_changes_filter(args)
    require = ((args.require or []) + changes)
    (include, exclude) = walk_external_targets(walk_compile_targets(), args.include, args.exclude, require)
    if (not include):
        raise AllTargetsSkipped()
    if args.delegate:
        raise Delegate(require=changes)
    install_command_requirements(args)
    version_commands = []
    for version in COMPILE_PYTHON_VERSIONS:
        if (args.python and (version != args.python)):
            continue
        skip_file = ('test/compile/python%s-skip.txt' % version)
        if os.path.exists(skip_file):
            with open(skip_file, 'r') as skip_fd:
                skip_paths = skip_fd.read().splitlines()
        else:
            skip_paths = []
        skip_paths += [e.path for e in exclude]
        skip_paths.append('/.tox/')
        skip_paths = sorted(skip_paths)
        python = ('python%s' % version)
        cmd = [python, '-m', 'compileall', '-fq']
        if skip_paths:
            cmd += ['-x', '|'.join(skip_paths)]
        cmd += [(target.path if (target.path == '.') else ('./%s' % target.path)) for target in include]
        version_commands.append((version, cmd))
    for (version, command) in version_commands:
        display.info(('Compile with Python %s' % version))
        run_command(args, command)

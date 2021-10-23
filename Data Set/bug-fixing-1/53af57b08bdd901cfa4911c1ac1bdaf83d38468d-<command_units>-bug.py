

def command_units(args):
    '\n    :type args: UnitsConfig\n    '
    changes = get_changes_filter(args)
    require = (args.require + changes)
    include = walk_internal_targets(walk_units_targets(), args.include, args.exclude, require)
    if (not include):
        raise AllTargetsSkipped()
    if args.delegate:
        raise Delegate(require=changes, exclude=args.exclude)
    version_commands = []
    available_versions = get_available_python_versions(SUPPORTED_PYTHON_VERSIONS)
    for version in SUPPORTED_PYTHON_VERSIONS:
        if (args.python and (version != args.python_version)):
            continue
        if ((not args.python) and (version not in available_versions)):
            display.warning(('Skipping unit tests on Python %s due to missing interpreter.' % version))
            continue
        if (args.requirements_mode != 'skip'):
            install_command_requirements(args, version)
        env = ansible_environment(args)
        cmd = ['pytest', '--boxed', '-r', 'a', '-n', (str(args.num_workers) if args.num_workers else 'auto'), '--color', ('yes' if args.color else 'no'), '--junit-xml', ('test/results/junit/python%s-units.xml' % version)]
        plugins = []
        if args.coverage:
            plugins.append('ansible_pytest_coverage')
        if data_context().content.collection:
            plugins.append('ansible_pytest_collections')
        if plugins:
            env['PYTHONPATH'] += (':%s' % os.path.join(ANSIBLE_ROOT, 'test/units/pytest/plugins'))
            for plugin in plugins:
                cmd.extend(['-p', plugin])
        if args.collect_only:
            cmd.append('--collect-only')
        if args.verbosity:
            cmd.append(('-' + ('v' * args.verbosity)))
        cmd += [target.path for target in include]
        version_commands.append((version, cmd, env))
    if (args.requirements_mode == 'only'):
        sys.exit()
    for (version, command, env) in version_commands:
        check_pyyaml(args, version)
        display.info(('Unit test with Python %s' % version))
        try:
            with coverage_context(args):
                intercept_command(args, command, target_name='units', env=env, python_version=version)
        except SubprocessError as ex:
            if (ex.status != 5):
                raise

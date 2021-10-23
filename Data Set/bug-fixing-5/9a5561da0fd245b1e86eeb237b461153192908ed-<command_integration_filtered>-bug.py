def command_integration_filtered(args, targets, all_targets):
    '\n    :type args: IntegrationConfig\n    :type targets: tuple[IntegrationTarget]\n    :type all_targets: tuple[IntegrationTarget]\n    '
    found = False
    passed = []
    failed = []
    targets_iter = iter(targets)
    all_targets_dict = dict(((target.name, target) for target in all_targets))
    setup_errors = []
    setup_targets_executed = set()
    for target in all_targets:
        for setup_target in (target.setup_once + target.setup_always):
            if (setup_target not in all_targets_dict):
                setup_errors.append(('Target "%s" contains invalid setup target: %s' % (target.name, setup_target)))
    if setup_errors:
        raise ApplicationError(('Found %d invalid setup aliases:\n%s' % (len(setup_errors), '\n'.join(setup_errors))))
    test_dir = os.path.expanduser('~/ansible_testing')
    if ((not args.explain) and any((('needs/ssh/' in target.aliases) for target in targets))):
        max_tries = 20
        display.info('SSH service required for tests. Checking to make sure we can connect.')
        for i in range(1, (max_tries + 1)):
            try:
                run_command(args, ['ssh', '-o', 'BatchMode=yes', 'localhost', 'id'], capture=True)
                display.info('SSH service responded.')
                break
            except SubprocessError:
                if (i == max_tries):
                    raise
                seconds = 3
                display.warning(('SSH service not responding. Waiting %d second(s) before checking again.' % seconds))
                time.sleep(seconds)
    if (args.inject_httptester and (not isinstance(args, WindowsIntegrationConfig))):
        inject_httptester(args)
    start_at_task = args.start_at_task
    results = {
        
    }
    current_environment = None
    for target in targets_iter:
        if (args.start_at and (not found)):
            found = (target.name == args.start_at)
            if (not found):
                continue
        if args.list_targets:
            print(target.name)
            continue
        tries = (2 if args.retry_on_error else 1)
        verbosity = args.verbosity
        cloud_environment = get_cloud_environment(args, target)
        original_environment = (current_environment if current_environment else EnvironmentDescription(args))
        current_environment = None
        display.info(('>>> Environment Description\n%s' % original_environment), verbosity=3)
        try:
            while tries:
                tries -= 1
                try:
                    if cloud_environment:
                        cloud_environment.setup_once()
                    run_setup_targets(args, test_dir, target.setup_once, all_targets_dict, setup_targets_executed, False)
                    start_time = time.time()
                    run_setup_targets(args, test_dir, target.setup_always, all_targets_dict, setup_targets_executed, True)
                    if (not args.explain):
                        remove_tree(test_dir)
                        make_dirs(test_dir)
                    if target.script_path:
                        command_integration_script(args, target, test_dir)
                    else:
                        command_integration_role(args, target, start_at_task, test_dir)
                        start_at_task = None
                    end_time = time.time()
                    results[target.name] = dict(name=target.name, type=target.type, aliases=target.aliases, modules=target.modules, run_time_seconds=int((end_time - start_time)), setup_once=target.setup_once, setup_always=target.setup_always, coverage=args.coverage, coverage_label=args.coverage_label, python_version=args.python_version)
                    break
                except SubprocessError:
                    if cloud_environment:
                        cloud_environment.on_failure(target, tries)
                    if (not original_environment.validate(target.name, throw=False)):
                        raise
                    if (not tries):
                        raise
                    display.warning(('Retrying test target "%s" with maximum verbosity.' % target.name))
                    display.verbosity = args.verbosity = 6
            start_time = time.time()
            current_environment = EnvironmentDescription(args)
            end_time = time.time()
            EnvironmentDescription.check(original_environment, current_environment, target.name, throw=True)
            results[target.name]['validation_seconds'] = int((end_time - start_time))
            passed.append(target)
        except Exception as ex:
            failed.append(target)
            if args.continue_on_error:
                display.error(ex)
                continue
            display.notice(('To resume at this test target, use the option: --start-at %s' % target.name))
            next_target = next(targets_iter, None)
            if next_target:
                display.notice(('To resume after this test target, use the option: --start-at %s' % next_target.name))
            raise
        finally:
            display.verbosity = args.verbosity = verbosity
    if (not args.explain):
        results_path = ('test/results/data/%s-%s.json' % (args.command, re.sub('[^0-9]', '-', str(datetime.datetime.utcnow().replace(microsecond=0)))))
        data = dict(targets=results)
        with open(results_path, 'w') as results_fd:
            results_fd.write(json.dumps(data, sort_keys=True, indent=4))
    if failed:
        raise ApplicationError(('The %d integration test(s) listed below (out of %d) failed. See error output above for details:\n%s' % (len(failed), (len(passed) + len(failed)), '\n'.join((target.name for target in failed)))))
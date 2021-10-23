def integration_environment(args, target, cmd, test_dir, inventory_path):
    '\n    :type args: IntegrationConfig\n    :type target: IntegrationTarget\n    :type cmd: list[str]\n    :type test_dir: str\n    :type inventory_path: str\n    :rtype: dict[str, str]\n    '
    env = ansible_environment(args)
    if args.inject_httptester:
        env.update(dict(HTTPTESTER='1'))
    integration = dict(JUNIT_OUTPUT_DIR=os.path.abspath('test/results/junit'), ANSIBLE_CALLBACK_WHITELIST='junit', ANSIBLE_TEST_CI=args.metadata.ci_provider, OUTPUT_DIR=test_dir, INVENTORY_PATH=os.path.abspath(inventory_path))
    if args.debug_strategy:
        env.update(dict(ANSIBLE_STRATEGY='debug'))
    if ('non_local/' in target.aliases):
        if args.coverage:
            display.warning(('Skipping coverage reporting for non-local test: %s' % target.name))
        env.update(dict(ANSIBLE_TEST_REMOTE_INTERPRETER=''))
    env.update(integration)
    cloud_environment = get_cloud_environment(args, target)
    if cloud_environment:
        cloud_environment.configure_environment(env, cmd)
    return env
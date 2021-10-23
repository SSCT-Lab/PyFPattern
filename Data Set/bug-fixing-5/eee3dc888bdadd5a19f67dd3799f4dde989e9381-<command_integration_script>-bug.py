def command_integration_script(args, target, test_dir):
    '\n    :type args: IntegrationConfig\n    :type target: IntegrationTarget\n    :type test_dir: str\n    '
    display.info(('Running %s integration test script' % target.name))
    cmd = [('./%s' % os.path.basename(target.script_path))]
    if args.verbosity:
        cmd.append(('-' + ('v' * args.verbosity)))
    env = integration_environment(args, target, cmd, test_dir)
    cwd = target.path
    intercept_command(args, cmd, target_name=target.name, env=env, cwd=cwd)
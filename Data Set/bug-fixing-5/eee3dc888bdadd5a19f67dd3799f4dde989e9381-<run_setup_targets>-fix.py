def run_setup_targets(args, test_dir, target_names, targets_dict, targets_executed, inventory_path, always):
    '\n    :type args: IntegrationConfig\n    :type test_dir: str\n    :type target_names: list[str]\n    :type targets_dict: dict[str, IntegrationTarget]\n    :type targets_executed: set[str]\n    :type inventory_path: str\n    :type always: bool\n    '
    for target_name in target_names:
        if ((not always) and (target_name in targets_executed)):
            continue
        target = targets_dict[target_name]
        if (not args.explain):
            remove_tree(test_dir)
            make_dirs(test_dir)
        if target.script_path:
            command_integration_script(args, target, test_dir, inventory_path)
        else:
            command_integration_role(args, target, None, test_dir, inventory_path)
        targets_executed.add(target_name)
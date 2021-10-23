def analyze_integration_target_dependencies(integration_targets):
    '\n    :type integration_targets: list[IntegrationTarget]\n    :rtype: dict[str,set[str]]\n    '
    real_target_root = (os.path.realpath('test/integration/targets') + '/')
    role_targets = [t for t in integration_targets if (t.type == 'role')]
    hidden_role_target_names = set((t.name for t in role_targets if ('hidden/' in t.aliases)))
    dependencies = collections.defaultdict(set)
    for target in integration_targets:
        for setup_target_name in (target.setup_always + target.setup_once):
            dependencies[setup_target_name].add(target.name)
    for target in integration_targets:
        for need_target in target.needs_target:
            dependencies[need_target].add(target.name)
    for target in integration_targets:
        for (root, _dummy, file_names) in os.walk(target.path):
            for name in file_names:
                path = os.path.join(root, name)
                if (not os.path.islink(path)):
                    continue
                real_link_path = os.path.realpath(path)
                if (not real_link_path.startswith(real_target_root)):
                    continue
                link_target = real_link_path[len(real_target_root):].split('/')[0]
                if (link_target == target.name):
                    continue
                dependencies[link_target].add(target.name)
    for target in integration_targets:
        meta_dir = os.path.join(target.path, 'meta')
        if (not os.path.isdir(meta_dir)):
            continue
        meta_paths = sorted([os.path.join(meta_dir, name) for name in os.listdir(meta_dir)])
        for meta_path in meta_paths:
            if os.path.exists(meta_path):
                with open(meta_path, 'rb') as meta_fd:
                    try:
                        meta_lines = meta_fd.read().decode('utf-8').splitlines()
                    except UnicodeDecodeError:
                        continue
                for meta_line in meta_lines:
                    if re.search('^ *#.*$', meta_line):
                        continue
                    if (not meta_line.strip()):
                        continue
                    for hidden_target_name in hidden_role_target_names:
                        if (hidden_target_name in meta_line):
                            dependencies[hidden_target_name].add(target.name)
    while True:
        changes = 0
        for (dummy, dependent_target_names) in dependencies.items():
            for dependent_target_name in list(dependent_target_names):
                new_target_names = dependencies.get(dependent_target_name)
                if new_target_names:
                    for new_target_name in new_target_names:
                        if (new_target_name not in dependent_target_names):
                            dependent_target_names.add(new_target_name)
                            changes += 1
        if (not changes):
            break
    for target_name in sorted(dependencies):
        consumers = dependencies[target_name]
        if (not consumers):
            continue
        display.info(('%s:' % target_name), verbosity=4)
        for consumer in sorted(consumers):
            display.info(('  %s' % consumer), verbosity=4)
    return dependencies
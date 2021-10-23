def categorize_changes(paths, verbose_command=None):
    '\n    :type paths: list[str]\n    :type verbose_command: str\n    :rtype paths: dict[str, list[str]]\n    '
    mapper = PathMapper()
    commands = {
        'sanity': set(),
        'compile': set(),
        'units': set(),
        'integration': set(),
        'windows-integration': set(),
        'network-integration': set(),
    }
    additional_paths = set()
    for path in paths:
        dependent_paths = mapper.get_dependent_paths(path)
        if (not dependent_paths):
            continue
        display.info(('Expanded "%s" to %d dependent file(s):' % (path, len(dependent_paths))), verbosity=1)
        for dependent_path in dependent_paths:
            display.info(dependent_path, verbosity=1)
            additional_paths.add(dependent_path)
    additional_paths -= set(paths)
    if additional_paths:
        display.info(('Expanded %d changed file(s) into %d additional dependent file(s).' % (len(paths), len(additional_paths))))
        paths = sorted((set(paths) | additional_paths))
    display.info(('Mapping %d changed file(s) to tests.' % len(paths)))
    for path in paths:
        tests = mapper.classify(path)
        if (tests is None):
            display.info(('%s -> all' % path), verbosity=1)
            tests = all_tests()
            display.warning(('Path not categorized: %s' % path))
        else:
            tests = dict(((key, value) for (key, value) in tests.items() if value))
            if verbose_command:
                result = ('%s: %s' % (verbose_command, (tests.get(verbose_command) or 'none')))
                if (('integration' in verbose_command) and tests.get(verbose_command)):
                    if (not any((('integration' in command) for command in tests if (command != verbose_command)))):
                        result += ' (targeted)'
            else:
                result = ('%s' % tests)
            display.info(('%s -> %s' % (path, result)), verbosity=1)
        for (command, target) in tests.items():
            commands[command].add(target)
    for command in commands:
        if any(((t == 'all') for t in commands[command])):
            commands[command] = set(['all'])
    commands = dict(((c, sorted(commands[c])) for c in commands if commands[c]))
    return commands
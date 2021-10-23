def test(self, args, targets):
    '\n        :type args: SanityConfig\n        :type targets: SanityTargets\n        :rtype: TestResult\n        '
    if (args.python_version in UNSUPPORTED_PYTHON_VERSIONS):
        display.warning(('Skipping pylint on unsupported Python version %s.' % args.python_version))
        return SanitySkipped(self.name)
    skip_paths = read_lines_without_comments(PYLINT_SKIP_PATH)
    invalid_ignores = []
    supported_versions = (set(SUPPORTED_PYTHON_VERSIONS) - set(UNSUPPORTED_PYTHON_VERSIONS))
    supported_versions = (set([v.split('.')[0] for v in supported_versions]) | supported_versions)
    ignore_entries = read_lines_without_comments(PYLINT_IGNORE_PATH)
    ignore = collections.defaultdict(dict)
    line = 0
    for ignore_entry in ignore_entries:
        line += 1
        if (not ignore_entry):
            continue
        if (' ' not in ignore_entry):
            invalid_ignores.append((line, 'Invalid syntax'))
            continue
        (path, code) = ignore_entry.split(' ', 1)
        if (not os.path.exists(path)):
            invalid_ignores.append((line, ('Remove "%s" since it does not exist' % path)))
            continue
        if (' ' in code):
            (code, version) = code.split(' ', 1)
            if (version not in supported_versions):
                invalid_ignores.append((line, ('Invalid version: %s' % version)))
                continue
            if (version not in (args.python_version, args.python_version.split('.')[0])):
                continue
        ignore[path][code] = line
    skip_paths_set = set(skip_paths)
    paths = sorted((i.path for i in targets.include if (((os.path.splitext(i.path)[1] == '.py') or i.path.startswith('bin/')) and (i.path not in skip_paths_set))))
    module_paths = [p.split(os.path.sep) for p in paths if p.startswith('lib/ansible/modules/')]
    module_dirs = sorted(set([p[3] for p in module_paths if (len(p) > 4)]))
    contexts = []
    remaining_paths = set(paths)

    def add_context(available_paths, context_name, context_filter):
        '\n            :type available_paths: set[str]\n            :type context_name: str\n            :type context_filter: (str) -> bool\n            '
        filtered_paths = set((p for p in available_paths if context_filter(p)))
        contexts.append((context_name, sorted(filtered_paths)))
        available_paths -= filtered_paths

    def filter_path(path_filter=None):
        '\n            :type path_filter: str\n            :rtype: (str) -> bool\n            '

        def context_filter(path_to_filter):
            '\n                :type path_to_filter: str\n                :rtype: bool\n                '
            return path_to_filter.startswith(path_filter)
        return context_filter
    add_context(remaining_paths, 'ansible-test', filter_path('test/runner/'))
    add_context(remaining_paths, 'units', filter_path('test/units/'))
    add_context(remaining_paths, 'test', filter_path('test/'))
    add_context(remaining_paths, 'hacking', filter_path('hacking/'))
    for module_dir in module_dirs:
        add_context(remaining_paths, ('modules/%s' % module_dir), filter_path(('lib/ansible/modules/%s/' % module_dir)))
    add_context(remaining_paths, 'modules', filter_path('lib/ansible/modules/'))
    add_context(remaining_paths, 'module_utils', filter_path('lib/ansible/module_utils/'))
    add_context(remaining_paths, 'ansible', (lambda p: True))
    messages = []
    context_times = []
    test_start = datetime.datetime.utcnow()
    for (context, context_paths) in sorted(contexts):
        if (not context_paths):
            continue
        context_start = datetime.datetime.utcnow()
        messages += self.pylint(args, context, context_paths)
        context_end = datetime.datetime.utcnow()
        context_times.append(('%s: %d (%s)' % (context, len(context_paths), (context_end - context_start))))
    test_end = datetime.datetime.utcnow()
    for context_time in context_times:
        display.info(context_time, verbosity=4)
    display.info(('total: %d (%s)' % (len(paths), (test_end - test_start))), verbosity=4)
    errors = [SanityMessage(message=m['message'].replace('\n', ' '), path=m['path'], line=int(m['line']), column=int(m['column']), level=m['type'], code=m['symbol']) for m in messages]
    if args.explain:
        return SanitySuccess(self.name)
    line = 0
    filtered = []
    for error in errors:
        if (error.code in ignore[error.path]):
            ignore[error.path][error.code] = None
        else:
            filtered.append(error)
    errors = filtered
    for invalid_ignore in invalid_ignores:
        errors.append(SanityMessage(code='A201', message=invalid_ignore[1], path=PYLINT_IGNORE_PATH, line=invalid_ignore[0], column=1, confidence=(calculate_confidence(PYLINT_IGNORE_PATH, line, args.metadata) if args.metadata.changes else None)))
    for path in skip_paths:
        line += 1
        if (not path):
            continue
        if (not os.path.exists(path)):
            errors.append(SanityMessage(code='A101', message=('Remove "%s" since it does not exist' % path), path=PYLINT_SKIP_PATH, line=line, column=1, confidence=(calculate_best_confidence(((PYLINT_SKIP_PATH, line), (path, 0)), args.metadata) if args.metadata.changes else None)))
    for path in paths:
        if (path not in ignore):
            continue
        for code in ignore[path]:
            line = ignore[path][code]
            if (not line):
                continue
            errors.append(SanityMessage(code='A102', message=('Remove since "%s" passes "%s" pylint test' % (path, code)), path=PYLINT_IGNORE_PATH, line=line, column=1, confidence=(calculate_best_confidence(((PYLINT_IGNORE_PATH, line), (path, 0)), args.metadata) if args.metadata.changes else None)))
    if errors:
        return SanityFailure(self.name, messages=errors)
    return SanitySuccess(self.name)
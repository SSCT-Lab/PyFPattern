def test(self, args, targets, python_version):
    '\n        :type args: SanityConfig\n        :type targets: SanityTargets\n        :type python_version: str\n        :rtype: TestResult\n        '
    skip_file = 'test/sanity/ansible-doc/skip.txt'
    skip_modules = set(read_lines_without_comments(skip_file, remove_blank_lines=True))
    plugin_type_blacklist = set(['action', 'doc_fragments', 'cliconf', 'filter', 'httpapi', 'netconf', 'terminal', 'test'])
    modules = sorted(((set((m for i in targets.include_external for m in i.modules)) - set((m for i in targets.exclude_external for m in i.modules))) - skip_modules))
    plugins = [(os.path.splitext(i.path)[0].split('/')[(- 2):] + [i.path]) for i in targets.include if ((os.path.splitext(i.path)[1] == '.py') and (os.path.basename(i.path) != '__init__.py') and re.search('^lib/ansible/plugins/[^/]+/', i.path) and (i.path != 'lib/ansible/plugins/cache/base.py'))]
    doc_targets = collections.defaultdict(list)
    target_paths = collections.defaultdict(dict)
    for module in modules:
        doc_targets['module'].append(module)
    for (plugin_type, plugin_name, plugin_path) in plugins:
        if (plugin_type in plugin_type_blacklist):
            continue
        doc_targets[plugin_type].append(plugin_name)
        target_paths[plugin_type][plugin_name] = plugin_path
    if (not doc_targets):
        return SanitySkipped(self.name, python_version=python_version)
    target_paths['module'] = dict(((t.module, t.path) for t in targets.targets if t.module))
    env = ansible_environment(args, color=False)
    error_messages = []
    for doc_type in sorted(doc_targets):
        cmd = (['ansible-doc', '-t', doc_type] + sorted(doc_targets[doc_type]))
        try:
            (stdout, stderr) = intercept_command(args, cmd, target_name='ansible-doc', env=env, capture=True, python_version=python_version)
            status = 0
        except SubprocessError as ex:
            stdout = ex.stdout
            stderr = ex.stderr
            status = ex.status
        if stderr:
            errors = stderr.strip().splitlines()
            messages = [self.parse_error(e, target_paths) for e in errors]
            if (messages and all(messages)):
                error_messages += messages
                continue
        if status:
            summary = ('%s' % SubprocessError(cmd=cmd, status=status, stderr=stderr))
            return SanityFailure(self.name, summary=summary, python_version=python_version)
        if stdout:
            display.info(stdout.strip(), verbosity=3)
        if stderr:
            summary = ('Output on stderr from ansible-doc is considered an error.\n\n%s' % SubprocessError(cmd, stderr=stderr))
            return SanityFailure(self.name, summary=summary, python_version=python_version)
    if error_messages:
        return SanityFailure(self.name, messages=error_messages, python_version=python_version)
    return SanitySuccess(self.name, python_version=python_version)
def walk_test_targets(path=None, module_path=None, extensions=None, prefix=None, extra_dirs=None):
    '\n    :type path: str | None\n    :type module_path: str | None\n    :type extensions: tuple[str] | None\n    :type prefix: str | None\n    :type extra_dirs: tuple[str] | None\n    :rtype: collections.Iterable[TestTarget]\n    '
    if path:
        file_paths = data_context().content.walk_files(path)
    else:
        file_paths = data_context().content.all_files()
    for file_path in file_paths:
        (name, ext) = os.path.splitext(os.path.basename(file_path))
        if (extensions and (ext not in extensions)):
            continue
        if (prefix and (not name.startswith(prefix))):
            continue
        if os.path.islink(file_path):
            if (file_path != 'lib/ansible/module_utils/ansible_release.py'):
                continue
        (yield TestTarget(file_path, module_path, prefix, path))
    file_paths = []
    if extra_dirs:
        for extra_dir in extra_dirs:
            for file_path in data_context().content.get_files(extra_dir):
                file_paths.append(file_path)
    for file_path in file_paths:
        if os.path.islink(file_path):
            continue
        (yield TestTarget(file_path, module_path, prefix, path))
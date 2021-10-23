def get_python_path(args, interpreter):
    '\n    :type args: TestConfig\n    :type interpreter: str\n    :rtype: str\n    '
    python_path = PYTHON_PATHS.get(interpreter)
    if python_path:
        return python_path
    prefix = 'python-'
    suffix = '-ansible'
    root_temp_dir = '/tmp'
    if args.explain:
        return os.path.join(root_temp_dir, ''.join((prefix, 'temp', suffix)))
    python_path = tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=root_temp_dir)
    os.chmod(python_path, MODE_DIRECTORY)
    os.symlink(interpreter, os.path.join(python_path, 'python'))
    if (not PYTHON_PATHS):
        atexit.register(cleanup_python_paths)
    PYTHON_PATHS[interpreter] = python_path
    return python_path
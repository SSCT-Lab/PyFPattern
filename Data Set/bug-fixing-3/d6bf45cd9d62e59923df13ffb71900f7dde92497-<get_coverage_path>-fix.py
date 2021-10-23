def get_coverage_path(args, version, interpreter):
    '\n    :type args: TestConfig\n    :type version: str\n    :type interpreter: str\n    :rtype: str\n    '
    coverage_path = COVERAGE_PATHS.get(version)
    if coverage_path:
        return os.path.join(coverage_path, 'coverage')
    prefix = ('ansible-test-coverage-python-%s-' % version)
    tmp_dir = '/tmp'
    if args.explain:
        return os.path.join(tmp_dir, ('%stmp' % prefix), 'coverage')
    src = os.path.abspath(os.path.join(os.getcwd(), 'test/runner/injector/'))
    coverage_path = tempfile.mkdtemp('', prefix, dir=tmp_dir)
    os.chmod(coverage_path, ((((stat.S_IRWXU | stat.S_IRGRP) | stat.S_IXGRP) | stat.S_IROTH) | stat.S_IXOTH))
    shutil.copytree(src, os.path.join(coverage_path, 'coverage'))
    shutil.copy('.coveragerc', os.path.join(coverage_path, 'coverage', '.coveragerc'))
    for (root, dir_names, file_names) in os.walk(coverage_path):
        for name in (dir_names + file_names):
            os.chmod(os.path.join(root, name), ((((stat.S_IRWXU | stat.S_IRGRP) | stat.S_IXGRP) | stat.S_IROTH) | stat.S_IXOTH))
    for directory in ('output', 'logs'):
        os.mkdir(os.path.join(coverage_path, directory))
        os.chmod(os.path.join(coverage_path, directory), ((stat.S_IRWXU | stat.S_IRWXG) | stat.S_IRWXO))
    os.symlink(interpreter, os.path.join(coverage_path, 'coverage', 'python'))
    if (not COVERAGE_PATHS):
        atexit.register(cleanup_coverage_dirs)
    COVERAGE_PATHS[version] = coverage_path
    return os.path.join(coverage_path, 'coverage')
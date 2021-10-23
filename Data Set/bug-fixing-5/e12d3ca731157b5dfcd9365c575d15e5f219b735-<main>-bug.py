def main():
    'Main entry point.'
    name = os.path.basename(__file__)
    args = [sys.executable]
    coverage_config = os.environ.get('_ANSIBLE_COVERAGE_CONFIG')
    coverage_output = os.environ.get('_ANSIBLE_COVERAGE_OUTPUT')
    if coverage_config:
        if coverage_output:
            args += ['-m', 'coverage.__main__', 'run', '--rcfile', coverage_config]
        else:
            try:
                imp.find_module('coverage')
            except ImportError:
                exit('ERROR: Could not find `coverage` module. Did you use a virtualenv created without --system-site-packages or with the wrong interpreter?')
    if (name == 'python.py'):
        if (sys.argv[1] == '-c'):
            sys.exit('ERROR: Use `python -c` instead of `python.py -c` to avoid errors when code coverage is collected.')
    elif (name == 'pytest'):
        args += ['-m', 'pytest']
    else:
        args += [find_executable(name)]
    args += sys.argv[1:]
    os.execv(args[0], args)
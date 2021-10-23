def get_python_path(args, interpreter):
    '\n    :type args: TestConfig\n    :type interpreter: str\n    :rtype: str\n    '
    if (os.path.basename(interpreter) == 'python'):
        return os.path.dirname(interpreter)
    python_path = PYTHON_PATHS.get(interpreter)
    if python_path:
        return python_path
    prefix = 'python-'
    suffix = '-ansible'
    root_temp_dir = '/tmp'
    if args.explain:
        return os.path.join(root_temp_dir, ''.join((prefix, 'temp', suffix)))
    python_path = tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=root_temp_dir)
    injected_interpreter = os.path.join(python_path, 'python')
    use_symlink = (os.path.dirname(os.path.realpath(interpreter)) == os.path.dirname(interpreter))
    if use_symlink:
        display.info(('Injecting "%s" as a symlink to the "%s" interpreter.' % (injected_interpreter, interpreter)), verbosity=1)
        os.symlink(interpreter, injected_interpreter)
    else:
        display.info(('Injecting "%s" as a execv wrapper for the "%s" interpreter.' % (injected_interpreter, interpreter)), verbosity=1)
        code = textwrap.dedent(("\n        #!%s\n\n        from __future__ import absolute_import\n\n        from os import execv\n        from sys import argv\n\n        python = '%s'\n\n        execv(python, [python] + argv[1:])\n        " % (interpreter, interpreter))).lstrip()
        with open(injected_interpreter, 'w') as python_fd:
            python_fd.write(code)
        os.chmod(injected_interpreter, MODE_FILE_EXECUTE)
    os.chmod(python_path, MODE_DIRECTORY)
    if (not PYTHON_PATHS):
        atexit.register(cleanup_python_paths)
    PYTHON_PATHS[interpreter] = python_path
    return python_path
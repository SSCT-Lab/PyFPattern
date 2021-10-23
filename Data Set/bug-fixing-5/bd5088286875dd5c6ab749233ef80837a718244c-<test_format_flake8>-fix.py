def test_format_flake8():
    '\n    Test if flake8 is respected.\n    '
    if (not flake8_available):
        raise SkipTest('flake8 is not installed')
    total_errors = 0
    for path in list_files():
        rel_path = os.path.relpath(path, theano.__path__[0])
        if (sys.platform == 'win32'):
            rel_path = rel_path.replace('\\', '/')
        if (rel_path in whitelist_flake8):
            continue
        else:
            error_num = flake8.main.check_file(path, ignore=ignore)
            total_errors += error_num
    if (total_errors > 0):
        raise AssertionError('FLAKE8 Format not respected')
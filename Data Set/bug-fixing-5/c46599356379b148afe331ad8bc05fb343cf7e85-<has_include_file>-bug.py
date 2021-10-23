def has_include_file(include_dirs, filename):
    '\n    Returns `True` if `filename` can be found in one of the\n    directories in `include_dirs`.\n    '
    if (sys.platform == 'win32'):
        include_dirs += os.environ.get('INCLUDE', '.').split(';')
    for dir in include_dirs:
        if os.path.exists(os.path.join(dir, filename)):
            return True
    return False
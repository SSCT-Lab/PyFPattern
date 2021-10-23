

def py_format(file_list=None):
    try:
        __import__('autopep8')
    except ImportError:
        print('[sentry.lint] Skipping Python autoformat because autopep8 is not installed.', err=True)
        return False
    py_file_list = get_python_files(file_list)
    return run_formatter(['autopep8', '--in-place', '-j0'], py_file_list)

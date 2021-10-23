def run_test(python, test_module, test_directory, verbose):
    verbose = ('--verbose' if verbose else '')
    return shell('{} {} {}'.format(python, test_module, verbose), test_directory)
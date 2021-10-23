def test_cpp_extensions(python, test_module, test_directory, verbose):
    if (not shell('{} setup.py install --root ./install'.format(python), os.path.join(test_directory, 'cpp_extensions'))):
        return False
    python_path = os.environ.get('PYTHONPATH', '')
    try:
        cpp_extensions = os.path.join(test_directory, 'cpp_extensions')
        install_directory = get_shell_output("find {}/install -name '*-packages'".format(cpp_extensions))
        install_directory = os.path.join(test_directory, install_directory)
        os.environ['PYTHONPATH'] = '{}:{}'.format(install_directory, python_path)
        return run_test(python, test_module, test_directory, verbose)
    finally:
        os.environ['PYTHONPATH'] = python_path
def test_cpp_extensions(python, test_module, test_directory, verbose):
    shell('{} setup.py install --root ./install'.format(python), os.path.join(test_directory, 'cpp_extensions'))
    python_path = os.environ.get('PYTHONPATH', '')
    install_directory = get_shell_output("find cpp_extensions/install -name '*-packages'")
    install_directory = os.path.join(test_directory, install_directory)
    os.environ['PYTHONPATH'] = '{}:{}'.format(install_directory, python_path)
    run_test(python, test_module, test_directory, verbose)
    os.environ['PYTHONPATH'] = python_path
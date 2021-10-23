def create_virtual_environment(args, version, path, system_site_packages=False, pip=True):
    'Create a virtual environment using venv or virtualenv for the requested Python version.'
    if os.path.isdir(path):
        display.info(('Using existing Python %s virtual environment: %s' % (version, path)), verbosity=1)
        return True
    python = find_python(version, required=False)
    python_version = tuple((int(v) for v in version.split('.')))
    if (not python):
        return False
    if (python_version >= (3, 0)):
        if run_venv(args, python, system_site_packages, pip, path):
            display.info(('Created Python %s virtual environment using "venv": %s' % (version, path)), verbosity=1)
            return True
        return False
    if run_virtualenv(args, python, python, system_site_packages, pip, path):
        display.info(('Created Python %s virtual environment using "virtualenv": %s' % (version, path)), verbosity=1)
        return True
    available_pythons = get_available_python_versions(SUPPORTED_PYTHON_VERSIONS)
    for (available_python_version, available_python_interpreter) in sorted(available_pythons.items()):
        virtualenv_version = get_virtualenv_version(args, available_python_interpreter)
        if (not virtualenv_version):
            continue
        if ((python_version == (2, 6)) and (virtualenv_version >= (16, 0, 0))):
            continue
        if run_virtualenv(args, available_python_interpreter, python, system_site_packages, pip, path):
            display.info(('Created Python %s virtual environment using "virtualenv" on Python %s: %s' % (version, available_python_version, path)), verbosity=1)
            return True
    return False
def run_virtualenv(args, run_python, env_python, system_site_packages, pip, path):
    "Create a virtual environment using the 'virtualenv' module."
    cmd = [run_python, '-m', 'virtualenv', '--python', env_python]
    if system_site_packages:
        cmd.append('--system-site-packages')
    if (not pip):
        cmd.append('--no-pip')
    cmd.append(path)
    try:
        run_command(args, cmd, capture=True)
    except SubprocessError:
        return False
    return True
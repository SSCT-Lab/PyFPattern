def run_venv(args, run_python, system_site_packages, pip, path):
    "Create a virtual environment using the 'venv' module. Not available on Python 2.x."
    cmd = [run_python, '-m', 'venv']
    if system_site_packages:
        cmd.append('--system-site-packages')
    if (not pip):
        cmd.append('--without-pip')
    cmd.append(path)
    try:
        run_command(args, cmd, capture=True)
    except SubprocessError:
        return False
    return True
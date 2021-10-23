def get_base_dirs():
    '\n    Returns a list of standard base directories on this platform.\n    '
    if options['basedirlist']:
        return options['basedirlist']
    if os.environ.get('MPLBASEDIRLIST'):
        return os.environ.get('MPLBASEDIRLIST').split(os.pathsep)
    win_bases = ['win32_static']
    conda_env_path = os.getenv('CONDA_PREFIX')
    if (not conda_env_path):
        conda_env_path = os.getenv('CONDA_DEFAULT_ENV')
    if (conda_env_path and os.path.isdir(conda_env_path)):
        win_bases.append(os.path.join(conda_env_path, 'Library'))
    basedir_map = {
        'win32': win_bases,
        'darwin': ['/usr/local/', '/usr', '/usr/X11', '/opt/X11', '/opt/local'],
        'sunos5': [(os.getenv('MPLIB_BASE') or '/usr/local')],
        'gnu0': ['/usr'],
        'aix5': ['/usr/local'],
    }
    return basedir_map.get(sys.platform, ['/usr/local', '/usr'])
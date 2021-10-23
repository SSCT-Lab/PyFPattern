@functools.lru_cache()
def _get_executable_info(name):
    '\n    Get the version of some executable that Matplotlib optionally depends on.\n\n    .. warning:\n       The list of executables that this function supports is set according to\n       Matplotlib\'s internal needs, and may change without notice.\n\n    Parameters\n    ----------\n    name : str\n        The executable to query.  The following values are currently supported:\n        "dvipng", "gs", "inkscape", "magick", "pdftops".  This list is subject\n        to change without notice.\n\n    Returns\n    -------\n    If the executable is found, a namedtuple with fields ``executable`` (`str`)\n    and ``version`` (`distutils.version.LooseVersion`, or ``None`` if the\n    version cannot be determined).\n\n    Raises\n    ------\n    FileNotFoundError\n        If the executable is not found or older than the oldest version\n        supported by Matplotlib.\n    ValueError\n        If the executable is not one that we know how to query.\n    '

    def impl(args, regex, min_ver=None):
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, universal_newlines=True)
        match = re.search(regex, output)
        if match:
            version = LooseVersion(match.group(1))
            if ((min_ver is not None) and (version < min_ver)):
                raise FileNotFoundError(f'You have {args[0]} version {version} but the minimum version supported by Matplotlib is {min_ver}.')
            return _ExecInfo(args[0], version)
        else:
            raise FileNotFoundError(f"Failed to determine the version of {args[0]} from {' '.join(args)}, which output {output}")
    if (name == 'dvipng'):
        return impl(['dvipng', '-version'], '(?m)^dvipng(?: .*)? (.+)', '1.6')
    elif (name == 'gs'):
        execs = (['gswin32c', 'gswin64c', 'mgs', 'gs'] if (sys.platform == 'win32') else ['gs'])
        for e in execs:
            try:
                return impl([e, '--version'], '(.*)', '9')
            except FileNotFoundError:
                pass
        raise FileNotFoundError('Failed to find a Ghostscript installation')
    elif (name == 'inkscape'):
        return impl(['inkscape', '-V'], '^Inkscape ([^ ]*)')
    elif (name == 'magick'):
        path = None
        if (sys.platform == 'win32'):
            import winreg
            binpath = ''
            for flag in [0, winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY]:
                try:
                    with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, 'Software\\Imagemagick\\Current', 0, (winreg.KEY_QUERY_VALUE | flag)) as hkey:
                        binpath = winreg.QueryValueEx(hkey, 'BinPath')[0]
                except OSError:
                    pass
            if binpath:
                for name in ['convert.exe', 'magick.exe']:
                    candidate = Path(binpath, name)
                    if candidate.exists():
                        path = str(candidate)
                        break
        else:
            path = 'convert'
        if (path is None):
            raise FileNotFoundError('Failed to find an ImageMagick installation')
        return impl([path, '--version'], '^Version: ImageMagick (\\S*)')
    elif (name == 'pdftops'):
        info = impl(['pdftops', '-v'], '^pdftops version (.*)')
        if (info and (not (('3.0' <= info.version) or ('0.9' <= info.version <= '1.0')))):
            raise FileNotFoundError(f'You have pdftops version {info.version} but the minimum version supported by Matplotlib is 3.0.')
        return info
    else:
        raise ValueError('Unknown executable: {!r}'.format(name))
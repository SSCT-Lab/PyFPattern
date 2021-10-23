def get_version(self, *args, **kwds):
    version = FCompiler.get_version(self, *args, **kwds)
    if ((version is None) and sys.platform.startswith('aix')):
        lslpp = find_executable('lslpp')
        xlf = find_executable('xlf')
        if (os.path.exists(xlf) and os.path.exists(lslpp)):
            try:
                o = subprocess.check_output([lslpp, '-Lc', 'xlfcmp'])
            except (OSError, subprocess.CalledProcessError):
                pass
            else:
                m = re.search('xlfcmp:(?P<version>\\d+([.]\\d+)+)', o)
                if m:
                    version = m.group('version')
    xlf_dir = '/etc/opt/ibmcmp/xlf'
    if ((version is None) and os.path.isdir(xlf_dir)):
        l = sorted(os.listdir(xlf_dir))
        l.reverse()
        l = [d for d in l if os.path.isfile(os.path.join(xlf_dir, d, 'xlf.cfg'))]
        if l:
            from distutils.version import LooseVersion
            self.version = version = LooseVersion(l[0])
    return version
def _get_svn_revision(self, path):
    "Return path's SVN revision number.\n        "
    revision = None
    m = None
    cwd = os.getcwd()
    try:
        os.chdir((path or '.'))
        p = subprocess.Popen(['svnversion'], shell=True, stdout=subprocess.PIPE, stderr=None, close_fds=True)
        sout = p.stdout
        m = re.match('(?P<revision>\\d+)', sout.read())
    except Exception:
        pass
    os.chdir(cwd)
    if m:
        revision = int(m.group('revision'))
        return revision
    if ((sys.platform == 'win32') and os.environ.get('SVN_ASP_DOT_NET_HACK', None)):
        entries = njoin(path, '_svn', 'entries')
    else:
        entries = njoin(path, '.svn', 'entries')
    if os.path.isfile(entries):
        f = open(entries)
        fstr = f.read()
        f.close()
        if (fstr[:5] == '<?xml'):
            m = re.search('revision="(?P<revision>\\d+)"', fstr)
            if m:
                revision = int(m.group('revision'))
        else:
            m = re.search('dir[\\n\\r]+(?P<revision>\\d+)', fstr)
            if m:
                revision = int(m.group('revision'))
    return revision
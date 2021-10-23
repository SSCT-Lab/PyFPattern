def _get_hg_revision(self, path):
    "Return path's Mercurial revision number.\n        "
    revision = None
    m = None
    cwd = os.getcwd()
    try:
        os.chdir((path or '.'))
        p = subprocess.Popen(['hg identify --num'], shell=True, stdout=subprocess.PIPE, stderr=None, close_fds=True)
        sout = p.stdout
        m = re.match('(?P<revision>\\d+)', sout.read())
    except Exception:
        pass
    os.chdir(cwd)
    if m:
        revision = int(m.group('revision'))
        return revision
    branch_fn = njoin(path, '.hg', 'branch')
    branch_cache_fn = njoin(path, '.hg', 'branch.cache')
    if os.path.isfile(branch_fn):
        branch0 = None
        f = open(branch_fn)
        revision0 = f.read().strip()
        f.close()
        branch_map = {
            
        }
        for line in file(branch_cache_fn, 'r'):
            (branch1, revision1) = line.split()[:2]
            if (revision1 == revision0):
                branch0 = branch1
            try:
                revision1 = int(revision1)
            except ValueError:
                continue
            branch_map[branch1] = revision1
        revision = branch_map.get(branch0)
    return revision
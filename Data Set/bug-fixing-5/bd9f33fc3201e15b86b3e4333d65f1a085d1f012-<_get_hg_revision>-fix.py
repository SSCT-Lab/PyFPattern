def _get_hg_revision(self, path):
    "Return path's Mercurial revision number.\n        "
    try:
        output = subprocess.check_output(['hg identify --num'], shell=True, cwd=path)
    except (subprocess.CalledProcessError, OSError):
        pass
    else:
        m = re.match(b'(?P<revision>\\d+)', output)
        if m:
            return int(m.group('revision'))
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
        return branch_map.get(branch0)
    return None
def _find_bind_mounts(self):
    bind_mounts = set()
    findmnt_path = self.module.get_bin_path('findmnt')
    if (not findmnt_path):
        return bind_mounts
    (rc, out, err) = self._run_findmnt(findmnt_path)
    if (rc != 0):
        return bind_mounts
    for line in out.splitlines():
        fields = line.split()
        if (len(fields) < 2):
            continue
        if self.BIND_MOUNT_RE.match(fields[1]):
            bind_mounts.add(fields[0])
    return bind_mounts
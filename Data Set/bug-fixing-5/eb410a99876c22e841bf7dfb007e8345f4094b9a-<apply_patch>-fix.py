def apply_patch(patch_func, patch_file, basedir, dest_file=None, binary=False, strip=0, dry_run=False, backup=False, state='present'):
    opts = ['--quiet', '--forward', '--batch', '--reject-file=-', ('--strip=%s' % strip), ("--directory='%s'" % basedir), ("--input='%s'" % patch_file)]
    if dry_run:
        add_dry_run_option(opts)
    if binary:
        opts.append('--binary')
    if dest_file:
        opts.append(("'%s'" % dest_file))
    if backup:
        opts.append('--backup --version-control=numbered')
    if (state == 'absent'):
        opts.append('--reverse')
    (rc, out, err) = patch_func(opts)
    if (rc != 0):
        msg = (err or out)
        raise PatchError(msg)
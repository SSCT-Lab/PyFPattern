def is_already_applied(patch_func, patch_file, basedir, dest_file=None, binary=False, strip=0, state='present'):
    opts = ['--quiet', '--forward', '--dry-run', ('--strip=%s' % strip), ("--directory='%s'" % basedir), ("--input='%s'" % patch_file)]
    if binary:
        opts.append('--binary')
    if dest_file:
        opts.append(("'%s'" % dest_file))
    if (state == 'present'):
        opts.append('--reverse')
    (rc, _, _) = patch_func(opts)
    return (rc == 0)
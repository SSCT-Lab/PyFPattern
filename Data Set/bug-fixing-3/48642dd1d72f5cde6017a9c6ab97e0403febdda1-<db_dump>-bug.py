def db_dump(module, host, user, password, db_name, target, all_databases, port, config_file, socket=None, ssl_cert=None, ssl_key=None, ssl_ca=None, single_transaction=None, quick=None, ignore_tables=None):
    cmd = module.get_bin_path('mysqldump', True)
    if config_file:
        cmd += (' --defaults-extra-file=%s' % pipes.quote(config_file))
    if (user is not None):
        cmd += (' --user=%s' % pipes.quote(user))
    if (password is not None):
        cmd += (' --password=%s' % pipes.quote(password))
    if (ssl_cert is not None):
        cmd += (' --ssl-cert=%s' % pipes.quote(ssl_cert))
    if (ssl_key is not None):
        cmd += (' --ssl-key=%s' % pipes.quote(ssl_key))
    if (ssl_cert is not None):
        cmd += (' --ssl-ca=%s' % pipes.quote(ssl_ca))
    if (socket is not None):
        cmd += (' --socket=%s' % pipes.quote(socket))
    else:
        cmd += (' --host=%s --port=%i' % (pipes.quote(host), port))
    if all_databases:
        cmd += ' --all-databases'
    else:
        cmd += (' %s' % pipes.quote(db_name))
    if single_transaction:
        cmd += ' --single-transaction=true'
    if quick:
        cmd += ' --quick'
    if ignore_tables:
        for an_ignored_table in ignore_tables:
            cmd += ' --ignore-table={0}'.format(an_ignored_table)
    path = None
    if (os.path.splitext(target)[(- 1)] == '.gz'):
        path = module.get_bin_path('gzip', True)
    elif (os.path.splitext(target)[(- 1)] == '.bz2'):
        path = module.get_bin_path('bzip2', True)
    elif (os.path.splitext(target)[(- 1)] == '.xz'):
        path = module.get_bin_path('xz', True)
    if path:
        cmd = ('%s | %s > %s' % (cmd, path, pipes.quote(target)))
    else:
        cmd += (' > %s' % pipes.quote(target))
    (rc, stdout, stderr) = module.run_command(cmd, use_unsafe_shell=True)
    return (rc, stdout, stderr)
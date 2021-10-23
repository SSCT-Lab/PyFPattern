

def db_import(module, host, user, password, db_name, target, all_databases, port, config_file, socket=None, ssl_cert=None, ssl_key=None, ssl_ca=None):
    if (not os.path.exists(target)):
        return module.fail_json(msg=('target %s does not exist on the host' % target))
    cmd = [module.get_bin_path('mysql', True)]
    if config_file:
        cmd.append(('--defaults-extra-file=%s' % shlex_quote(config_file)))
    if user:
        cmd.append(('--user=%s' % shlex_quote(user)))
    if password:
        cmd.append(('--password=%s' % shlex_quote(password)))
    if (ssl_cert is not None):
        cmd.append(('--ssl-cert=%s' % shlex_quote(ssl_cert)))
    if (ssl_key is not None):
        cmd.append(('--ssl-key=%s' % shlex_quote(ssl_key)))
    if (ssl_ca is not None):
        cmd.append(('--ssl-ca=%s' % shlex_quote(ssl_ca)))
    if (socket is not None):
        cmd.append(('--socket=%s' % shlex_quote(socket)))
    else:
        cmd.append(('--host=%s' % shlex_quote(host)))
        cmd.append(('--port=%i' % port))
    if (not all_databases):
        cmd.append('--one-database')
        cmd.append(shlex_quote(''.join(db_name)))
    comp_prog_path = None
    if (os.path.splitext(target)[(- 1)] == '.gz'):
        comp_prog_path = module.get_bin_path('gzip', required=True)
    elif (os.path.splitext(target)[(- 1)] == '.bz2'):
        comp_prog_path = module.get_bin_path('bzip2', required=True)
    elif (os.path.splitext(target)[(- 1)] == '.xz'):
        comp_prog_path = module.get_bin_path('xz', required=True)
    if comp_prog_path:
        p1 = subprocess.Popen([comp_prog_path, '-dc', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(cmd, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout2, stderr2) = p2.communicate()
        p1.stdout.close()
        p1.wait()
        if (p1.returncode != 0):
            stderr1 = p1.stderr.read()
            return (p1.returncode, '', stderr1)
        else:
            return (p2.returncode, stdout2, stderr2)
    else:
        cmd = ' '.join(cmd)
        cmd += (' < %s' % shlex_quote(target))
        (rc, stdout, stderr) = module.run_command(cmd, use_unsafe_shell=True)
        return (rc, stdout, stderr)

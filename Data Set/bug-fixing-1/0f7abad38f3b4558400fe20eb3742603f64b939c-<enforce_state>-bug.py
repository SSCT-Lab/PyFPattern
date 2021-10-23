

def enforce_state(module, params):
    '\n    Add or remove key.\n    '
    host = params['name']
    key = params.get('key', None)
    port = params.get('port', None)
    path = params.get('path')
    hash_host = params.get('hash_host')
    state = params.get('state')
    sshkeygen = module.get_bin_path('ssh-keygen', True)
    if (key and (key[(- 1)] != '\n')):
        key += '\n'
    if ((key is None) and (state != 'absent')):
        module.fail_json(msg='No key specified when adding a host')
    sanity_check(module, host, key, sshkeygen)
    (found, replace_or_add, found_line, key) = search_for_host_key(module, host, key, hash_host, path, sshkeygen)
    if module.check_mode:
        module.exit_json(changed=(replace_or_add or ((state == 'present') != found)))
    if (found and (key is None) and (state == 'absent')):
        module.run_command([sshkeygen, '-R', host, '-f', path], check_rc=True)
        params['changed'] = True
    if (replace_or_add or (found != (state == 'present'))):
        try:
            inf = open(path, 'r')
        except IOError:
            e = get_exception()
            if (e.errno == errno.ENOENT):
                inf = None
            else:
                module.fail_json(msg=('Failed to read %s: %s' % (path, str(e))))
        try:
            outf = tempfile.NamedTemporaryFile(dir=os.path.dirname(path))
            if (inf is not None):
                for (line_number, line) in enumerate(inf, start=1):
                    if ((found_line == line_number) and (replace_or_add or (state == 'absent'))):
                        continue
                    outf.write(line)
                inf.close()
            if (state == 'present'):
                outf.write(key)
            outf.flush()
            module.atomic_move(outf.name, path)
        except (IOError, OSError):
            e = get_exception()
            module.fail_json(msg=('Failed to write to file %s: %s' % (path, str(e))))
        try:
            outf.close()
        except:
            pass
        params['changed'] = True
    return params

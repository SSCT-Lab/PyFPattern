def search_for_host_key(module, host, key, hash_host, path, sshkeygen):
    "search_for_host_key(module,host,key,path,sshkeygen) -> (found,replace_or_add,found_line)\n\n    Looks up host and keytype in the known_hosts file path; if it's there, looks to see\n    if one of those entries matches key. Returns:\n    found (Boolean): is host found in path?\n    replace_or_add (Boolean): is the key in path different to that supplied by user?\n    found_line (int or None): the line where a key of the same type was found\n    if found=False, then replace is always False.\n    sshkeygen is the path to ssh-keygen, found earlier with get_bin_path\n    "
    if (os.path.exists(path) == False):
        return (False, False, None, key)
    sshkeygen_command = [sshkeygen, '-F', host, '-f', path]
    (rc, stdout, stderr) = module.run_command(sshkeygen_command, check_rc=False)
    if ((stdout == '') and (stderr == '') and ((rc == 0) or (rc == 1))):
        return (False, False, None, key)
    if (rc != 0):
        module.fail_json(msg=("ssh-keygen failed (rc=%d,stdout='%s',stderr='%s')" % (rc, stdout, stderr)))
    if (key is None):
        return (True, False, None, key)
    lines = stdout.split('\n')
    new_key = normalize_known_hosts_key(key)
    sshkeygen_command.insert(1, '-H')
    (rc, stdout, stderr) = module.run_command(sshkeygen_command, check_rc=False)
    if (rc != 0):
        module.fail_json(msg=("ssh-keygen failed to hash host (rc=%d,stdout='%s',stderr='%s')" % (rc, stdout, stderr)))
    hashed_lines = stdout.split('\n')
    for (lnum, l) in enumerate(lines):
        if (l == ''):
            continue
        elif (l[0] == '#'):
            try:
                found_line = int(re.search('found: line (\\d+)', l).group(1))
            except IndexError:
                e = get_exception()
                module.fail_json(msg=("failed to parse output of ssh-keygen for line number: '%s'" % l))
        else:
            found_key = normalize_known_hosts_key(l)
            if (hash_host == True):
                if (found_key['host'][:3] == '|1|'):
                    new_key['host'] = found_key['host']
                else:
                    hashed_host = normalize_known_hosts_key(hashed_lines[lnum])
                    found_key['host'] = hashed_host['host']
                key = key.replace(host, found_key['host'])
            if (new_key == found_key):
                return (True, False, found_line, key)
            elif (new_key['type'] == found_key['type']):
                return (True, True, found_line, key)
    return (True, True, None, key)
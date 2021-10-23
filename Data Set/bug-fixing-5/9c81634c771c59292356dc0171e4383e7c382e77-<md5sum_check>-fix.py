def md5sum_check(module, dst, file_system):
    command = 'show file {0}{1} md5sum'.format(file_system, dst)
    remote_filehash = run_commands(module, {
        'command': command,
        'output': 'text',
    })[0]
    remote_filehash = to_bytes(remote_filehash, errors='surrogate_or_strict')
    local_file = module.params['local_file']
    try:
        with open(local_file, 'rb') as f:
            filecontent = f.read()
    except (OSError, IOError) as exc:
        module.fail_json(msg=('Error reading the file: %s' % to_text(exc)))
    filecontent = to_bytes(filecontent, errors='surrogate_or_strict')
    local_filehash = hashlib.md5(filecontent).hexdigest()
    if (local_filehash == remote_filehash):
        return True
    else:
        return False
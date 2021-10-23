def all_keys(module, keyring, short_format):
    if keyring:
        cmd = ('%s --keyring %s adv --list-public-keys --keyid-format=long' % (apt_key_bin, keyring))
    else:
        cmd = ('%s adv --list-public-keys --keyid-format=long' % apt_key_bin)
    (rc, out, err) = module.run_command(cmd)
    results = []
    lines = to_native(out).split('\n')
    for line in lines:
        if (line.startswith('pub') or line.startswith('sub')):
            tokens = line.split()
            code = tokens[1]
            (len_type, real_code) = code.split('/')
            results.append(real_code)
    if short_format:
        results = shorten_key_ids(results)
    return results
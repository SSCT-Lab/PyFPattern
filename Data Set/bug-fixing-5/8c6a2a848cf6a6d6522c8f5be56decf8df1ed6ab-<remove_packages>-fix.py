def remove_packages(module, pacman_path, packages):
    data = []
    diff = {
        'before': '',
        'after': '',
    }
    if (module.params['recurse'] or module.params['force']):
        if module.params['recurse']:
            args = 'Rs'
        if module.params['force']:
            args = 'Rdd'
        if (module.params['recurse'] and module.params['force']):
            args = 'Rdds'
    else:
        args = 'R'
    remove_c = 0
    for package in packages:
        (installed, updated, unknown) = query_package(module, pacman_path, package)
        if (not installed):
            continue
        cmd = ('%s -%s %s --noconfirm --noprogressbar' % (pacman_path, args, package))
        (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
        if (rc != 0):
            module.fail_json(msg=('failed to remove %s' % package))
        if module._diff:
            d = stdout.split('\n')[2].split(' ')[2:]
            for (i, pkg) in enumerate(d):
                d[i] = re.sub('-[0-9].*$', '', d[i].split('/')[(- 1)])
                diff['before'] += ('%s\n' % pkg)
            data.append('\n'.join(d))
        remove_c += 1
    if (remove_c > 0):
        module.exit_json(changed=True, msg=('removed %s package(s)' % remove_c), diff=diff)
    module.exit_json(changed=False, msg='package(s) already absent')
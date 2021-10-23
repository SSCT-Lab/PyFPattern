def install_packages(module, pacman_path, state, packages, package_files):
    install_c = 0
    package_err = []
    message = ''
    data = []
    diff = {
        'before': '',
        'after': '',
    }
    to_install_repos = []
    to_install_files = []
    for (i, package) in enumerate(packages):
        (installed, updated, latestError) = query_package(module, pacman_path, package)
        if (latestError and (state == 'latest')):
            package_err.append(package)
        if (installed and ((state == 'present') or ((state == 'latest') and updated))):
            continue
        if package_files[i]:
            to_install_files.append(package_files[i])
        else:
            to_install_repos.append(package)
    if to_install_repos:
        cmd = ('%s -S %s --noconfirm --noprogressbar --needed' % (pacman_path, ' '.join(to_install_repos)))
        (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
        if (rc != 0):
            module.fail_json(msg=('failed to install %s: %s' % (' '.join(to_install_repos), stderr)))
        data = stdout.split('\n')[3].split(' ')[2:]
        data = [i for i in data if (i != '')]
        for (i, pkg) in enumerate(data):
            data[i] = re.sub('-[0-9].*$', '', data[i].split('/')[(- 1)])
            if module._diff:
                diff['after'] += ('%s\n' % pkg)
        install_c += len(to_install_repos)
    if to_install_files:
        cmd = ('%s -U %s --noconfirm --noprogressbar --needed' % (pacman_path, ' '.join(to_install_files)))
        (rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
        if (rc != 0):
            module.fail_json(msg=('failed to install %s: %s' % (' '.join(to_install_files), stderr)))
        data = stdout.split('\n')[3].split(' ')[2:]
        data = [i for i in data if (i != '')]
        for (i, pkg) in enumerate(data):
            data[i] = re.sub('-[0-9].*$', '', data[i].split('/')[(- 1)])
            if module._diff:
                diff['after'] += ('%s\n' % pkg)
        install_c += len(to_install_files)
    if ((state == 'latest') and (len(package_err) > 0)):
        message = ("But could not ensure 'latest' state for %s package(s) as remote version could not be fetched." % package_err)
    if (install_c > 0):
        module.exit_json(changed=True, msg=('installed %s package(s). %s' % (install_c, message)), diff=diff)
    module.exit_json(changed=False, msg=('package(s) already installed. %s' % message), diff=diff)
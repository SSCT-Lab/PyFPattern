def emerge_packages(module, packages):
    p = module.params
    if (not (p['update'] or p['noreplace'] or (p['state'] == 'latest'))):
        for package in packages:
            if (not query_package(module, package, 'emerge')):
                break
        else:
            module.exit_json(changed=False, msg='Packages already present.')
        if module.check_mode:
            module.exit_json(changed=True, msg='Packages would be installed.')
    args = []
    emerge_flags = {
        'update': '--update',
        'deep': '--deep',
        'newuse': '--newuse',
        'changed_use': '--changed-use',
        'oneshot': '--oneshot',
        'noreplace': '--noreplace',
        'nodeps': '--nodeps',
        'onlydeps': '--onlydeps',
        'quiet': '--quiet',
        'verbose': '--verbose',
        'getbinpkg': '--getbinpkg',
        'usepkgonly': '--usepkgonly',
        'usepkg': '--usepkg',
        'keepgoing': '--keep-going',
    }
    for (flag, arg) in emerge_flags.items():
        if p[flag]:
            args.append(arg)
    if (p['state'] and (p['state'] == 'latest')):
        args.append('--update')
    if (p['usepkg'] and p['usepkgonly']):
        module.fail_json(msg='Use only one of usepkg, usepkgonly')
    emerge_flags = {
        'jobs': '--jobs=',
        'loadavg': '--load-average ',
    }
    for (flag, arg) in emerge_flags.items():
        if (p[flag] is not None):
            args.append((arg + str(p[flag])))
    (cmd, (rc, out, err)) = run_emerge(module, packages, *args)
    if (rc != 0):
        module.fail_json(cmd=cmd, rc=rc, stdout=out, stderr=err, msg='Packages not installed.')
    if ((p['usepkgonly'] or p['getbinpkg']) and ('Permission denied (publickey).' in err)):
        module.fail_json(cmd=cmd, rc=rc, stdout=out, stderr=err, msg='Please check your PORTAGE_BINHOST configuration in make.conf and your SSH authorized_keys file')
    changed = True
    for line in out.splitlines():
        if re.match('(?:>+) Emerging (?:binary )?\\(1 of', line):
            msg = 'Packages installed.'
            break
        elif (module.check_mode and re.match('\\[(binary|ebuild)', line)):
            msg = 'Packages would be installed.'
            break
    else:
        changed = False
        msg = 'No packages installed.'
    module.exit_json(changed=changed, cmd=cmd, rc=rc, stdout=out, stderr=err, msg=msg)
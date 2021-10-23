def latest(module, items, repoq, yum_basecmd, conf_file, en_repos, dis_repos, update_only, installroot='/'):
    res = {
        
    }
    res['results'] = []
    res['msg'] = ''
    res['changed'] = False
    res['rc'] = 0
    pkgs = {
        
    }
    pkgs['update'] = []
    pkgs['install'] = []
    updates = {
        
    }
    update_all = False
    cmd = None
    if ('*' in items):
        update_all = True
    (rc, out, err) = run_check_update(module, yum_basecmd)
    if ((rc == 0) and update_all):
        res['results'].append('Nothing to do here, all packages are up to date')
        return res
    elif (rc == 100):
        updates = parse_check_update(out)
    elif (rc == 1):
        res['msg'] = err
        res['rc'] = rc
        module.fail_json(**res)
    if update_all:
        cmd = (yum_basecmd + ['update'])
        will_update = set(updates.keys())
        will_update_from_other_package = dict()
    else:
        will_update = set()
        will_update_from_other_package = dict()
        for spec in items:
            if spec.startswith('@'):
                pkgs['update'].append(spec)
                will_update.add(spec)
                continue
            elif (spec.endswith('.rpm') and ('://' not in spec)):
                if (not os.path.exists(spec)):
                    res['msg'] += ("No RPM file matching '%s' found on system" % spec)
                    res['results'].append(("No RPM file matching '%s' found on system" % spec))
                    res['rc'] = 127
                    module.fail_json(**res)
                envra = local_envra(spec)
                if (not is_installed(module, repoq, envra, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)):
                    pkgs['install'].append(spec)
                continue
            elif ('://' in spec):
                package = fetch_rpm_from_url(spec, module=module)
                envra = local_envra(package)
                if (not is_installed(module, repoq, envra, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)):
                    pkgs['install'].append(package)
                continue
            elif (is_installed(module, repoq, spec, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot) or update_only):
                pkgs['update'].append(spec)
            else:
                pkgs['install'].append(spec)
            pkglist = what_provides(module, repoq, spec, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)
            if (not pkglist):
                res['msg'] += ("No package matching '%s' found available, installed or updated" % spec)
                res['results'].append(("No package matching '%s' found available, installed or updated" % spec))
                res['rc'] = 126
                module.fail_json(**res)
            nothing_to_do = True
            for pkg in pkglist:
                if ((spec in pkgs['install']) and is_available(module, repoq, pkg, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)):
                    nothing_to_do = False
                    break
                (pkgname, _, _, _, _) = splitFilename(pkg)
                if ((spec in pkgs['update']) and (pkgname in updates)):
                    nothing_to_do = False
                    will_update.add(spec)
                    if (spec != pkgname):
                        will_update_from_other_package[spec] = pkgname
                    break
            if ((not is_installed(module, repoq, spec, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)) and update_only):
                res['results'].append(('Packages providing %s not installed due to update_only specified' % spec))
                continue
            if nothing_to_do:
                res['results'].append(('All packages providing %s are up to date' % spec))
                continue
            conflicts = transaction_exists(pkglist)
            if conflicts:
                res['msg'] += ('The following packages have pending transactions: %s' % ', '.join(conflicts))
                res['results'].append(('The following packages have pending transactions: %s' % ', '.join(conflicts)))
                res['rc'] = 128
                module.fail_json(**res)
    if module.check_mode:
        to_update = []
        for w in will_update:
            if w.startswith('@'):
                to_update.append((w, None))
            elif (w not in updates):
                other_pkg = will_update_from_other_package[w]
                to_update.append((w, ('because of (at least) %s-%s.%s from %s' % (other_pkg, updates[other_pkg]['version'], updates[other_pkg]['dist'], updates[other_pkg]['repo']))))
            else:
                to_update.append((w, ('%s.%s from %s' % (updates[w]['version'], updates[w]['dist'], updates[w]['repo']))))
        res['changes'] = dict(installed=pkgs['install'], updated=to_update)
        if (will_update or pkgs['install']):
            res['changed'] = True
        return res
    if cmd:
        (rc, out, err) = module.run_command(cmd)
        res['changed'] = True
    elif (pkgs['install'] or will_update):
        cmd = (((yum_basecmd + ['install']) + pkgs['install']) + pkgs['update'])
        lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
        (rc, out, err) = module.run_command(cmd, environ_update=lang_env)
        out_lower = out.strip().lower()
        if ((not out_lower.endswith('no packages marked for update')) and (not out_lower.endswith('nothing to do'))):
            res['changed'] = True
    else:
        (rc, out, err) = [0, '', '']
    res['rc'] = rc
    res['msg'] += err
    res['results'].append(out)
    if rc:
        res['failed'] = True
    return res
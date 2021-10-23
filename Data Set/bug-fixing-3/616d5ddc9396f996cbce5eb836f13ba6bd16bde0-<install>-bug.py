def install(module, items, repoq, yum_basecmd, conf_file, en_repos, dis_repos, installroot='/'):
    pkgs = []
    res = {
        
    }
    res['results'] = []
    res['msg'] = ''
    res['rc'] = 0
    res['changed'] = False
    tempdir = tempfile.mkdtemp()
    for spec in items:
        pkg = None
        if (spec.endswith('.rpm') and ('://' not in spec)):
            if (not os.path.exists(spec)):
                res['msg'] += ("No RPM file matching '%s' found on system" % spec)
                res['results'].append(("No RPM file matching '%s' found on system" % spec))
                res['rc'] = 127
                module.fail_json(**res)
            nvra = local_nvra(module, spec)
            if is_installed(module, repoq, nvra, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot):
                continue
            pkg = spec
        elif ('://' in spec):
            package = fetch_rpm_from_url(spec, module=module)
            nvra = local_nvra(module, package)
            if is_installed(module, repoq, nvra, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot):
                continue
            pkg = package
        elif spec.startswith('@'):
            pkg = spec
        else:
            if (not set(['*', '?']).intersection(set(spec))):
                installed_pkgs = is_installed(module, repoq, spec, conf_file, en_repos=en_repos, dis_repos=dis_repos, is_pkg=True, installroot=installroot)
                if installed_pkgs:
                    res['results'].append(('%s providing %s is already installed' % (installed_pkgs[0], spec)))
                    continue
            pkglist = what_provides(module, repoq, spec, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)
            if (not pkglist):
                res['msg'] += ("No package matching '%s' found available, installed or updated" % spec)
                res['results'].append(("No package matching '%s' found available, installed or updated" % spec))
                res['rc'] = 126
                module.fail_json(**res)
            conflicts = transaction_exists(pkglist)
            if (len(conflicts) > 0):
                res['msg'] += ('The following packages have pending transactions: %s' % ', '.join(conflicts))
                res['rc'] = 125
                module.fail_json(**res)
            found = False
            for this in pkglist:
                if is_installed(module, repoq, this, conf_file, en_repos=en_repos, dis_repos=dis_repos, is_pkg=True, installroot=installroot):
                    found = True
                    res['results'].append(('%s providing %s is already installed' % (this, spec)))
                    break
            if (not found):
                if is_installed(module, repoq, spec, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot):
                    found = True
                    res['results'].append(('package providing %s is already installed' % spec))
            if found:
                continue
            pkg = spec
        pkgs.append(pkg)
    if pkgs:
        cmd = ((yum_basecmd + ['install']) + pkgs)
        if module.check_mode:
            try:
                shutil.rmtree(tempdir)
            except Exception:
                e = get_exception()
                module.fail_json(msg=('Failure deleting temp directory %s, %s' % (tempdir, e)))
            module.exit_json(changed=True, results=res['results'], changes=dict(installed=pkgs))
        changed = True
        lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
        (rc, out, err) = module.run_command(cmd, environ_update=lang_env)
        if (rc == 1):
            for spec in items:
                if (('://' in spec) and ((('No package %s available.' % spec) in out) or (('Cannot open: %s. Skipping.' % spec) in err))):
                    module.fail_json(msg=('Package at %s could not be installed' % spec), rc=1, changed=False)
        if (((rc != 0) and ('Nothing to do' in err)) or ('Nothing to do' in out)):
            rc = 0
            err = ''
            out = ('%s: Nothing to do' % spec)
            changed = False
        res['rc'] = rc
        res['results'].append(out)
        res['msg'] += err
        res['changed'] = changed
    try:
        shutil.rmtree(tempdir)
    except Exception:
        e = get_exception()
        module.fail_json(msg=('Failure deleting temp directory %s, %s' % (tempdir, e)))
    return res
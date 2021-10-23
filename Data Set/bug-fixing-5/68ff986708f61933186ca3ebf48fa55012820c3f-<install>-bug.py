def install(module, items, repoq, yum_basecmd, conf_file, en_repos, dis_repos, installroot='/', allow_downgrade=False):
    pkgs = []
    downgrade_pkgs = []
    res = {
        
    }
    res['results'] = []
    res['msg'] = ''
    res['rc'] = 0
    res['changed'] = False
    for spec in items:
        pkg = None
        downgrade_candidate = False
        if spec.endswith('.rpm'):
            if (('://' not in spec) and (not os.path.exists(spec))):
                res['msg'] += ("No RPM file matching '%s' found on system" % spec)
                res['results'].append(("No RPM file matching '%s' found on system" % spec))
                res['rc'] = 127
                module.fail_json(**res)
            if ('://' in spec):
                with set_env_proxy(conf_file, installroot):
                    package = fetch_rpm_from_url(spec, module=module)
            else:
                package = spec
            envra = local_envra(package)
            if (envra is None):
                module.fail_json(msg=('Failed to get nevra information from RPM package: %s' % spec))
            installed_pkgs = is_installed(module, repoq, envra, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)
            if installed_pkgs:
                res['results'].append(('%s providing %s is already installed' % (installed_pkgs[0], package)))
                continue
            (name, ver, rel, epoch, arch) = splitFilename(envra)
            installed_pkgs = is_installed(module, repoq, name, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)
            if (len(installed_pkgs) == 2):
                (cur_name0, cur_ver0, cur_rel0, cur_epoch0, cur_arch0) = splitFilename(installed_pkgs[0])
                (cur_name1, cur_ver1, cur_rel1, cur_epoch1, cur_arch1) = splitFilename(installed_pkgs[1])
                cur_epoch0 = (cur_epoch0 or '0')
                cur_epoch1 = (cur_epoch1 or '0')
                compare = compareEVR((cur_epoch0, cur_ver0, cur_rel0), (cur_epoch1, cur_ver1, cur_rel1))
                if ((compare == 0) and (cur_arch0 != cur_arch1)):
                    for installed_pkg in installed_pkgs:
                        if installed_pkg.endswith(arch):
                            installed_pkgs = [installed_pkg]
            if (len(installed_pkgs) == 1):
                installed_pkg = installed_pkgs[0]
                (cur_name, cur_ver, cur_rel, cur_epoch, cur_arch) = splitFilename(installed_pkg)
                cur_epoch = (cur_epoch or '0')
                compare = compareEVR((cur_epoch, cur_ver, cur_rel), (epoch, ver, rel))
                if ((compare > 0) and allow_downgrade):
                    downgrade_candidate = True
                elif (compare >= 0):
                    continue
            pkg = package
        elif spec.startswith('@'):
            if is_group_env_installed(spec, conf_file, installroot=installroot):
                continue
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
            if conflicts:
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
            if allow_downgrade:
                for package in pkglist:
                    (name, ver, rel, epoch, arch) = splitFilename(package)
                    inst_pkgs = is_installed(module, repoq, name, conf_file, en_repos=en_repos, dis_repos=dis_repos, is_pkg=True)
                    if inst_pkgs:
                        (cur_name, cur_ver, cur_rel, cur_epoch, cur_arch) = splitFilename(inst_pkgs[0])
                        compare = compareEVR((cur_epoch, cur_ver, cur_rel), (epoch, ver, rel))
                        if (compare > 0):
                            downgrade_candidate = True
                        else:
                            downgrade_candidate = False
                            break
            pkg = spec
        if (downgrade_candidate and allow_downgrade):
            downgrade_pkgs.append(pkg)
        else:
            pkgs.append(pkg)
    if downgrade_pkgs:
        res = exec_install(module, items, 'downgrade', downgrade_pkgs, res, yum_basecmd)
    if pkgs:
        res = exec_install(module, items, 'install', pkgs, res, yum_basecmd)
    return res
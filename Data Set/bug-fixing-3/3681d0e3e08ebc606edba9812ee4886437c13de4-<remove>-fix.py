def remove(module, items, repoq, yum_basecmd, conf_file, en_repos, dis_repos, installroot='/'):
    pkgs = []
    res = {
        
    }
    res['results'] = []
    res['msg'] = ''
    res['changed'] = False
    res['rc'] = 0
    for pkg in items:
        if pkg.startswith('@'):
            installed = is_group_env_installed(pkg, conf_file, installroot=installroot)
        else:
            installed = is_installed(module, repoq, pkg, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)
        if installed:
            pkgs.append(pkg)
        else:
            res['results'].append(('%s is not installed' % pkg))
    if pkgs:
        if module.check_mode:
            module.exit_json(changed=True, results=res['results'], changes=dict(removed=pkgs))
        cmd = ((yum_basecmd + ['remove']) + pkgs)
        (rc, out, err) = module.run_command(cmd)
        res['rc'] = rc
        res['results'].append(out)
        res['msg'] = err
        if (rc != 0):
            module.fail_json(**res)
        for pkg in pkgs:
            if pkg.startswith('@'):
                installed = is_group_env_installed(pkg, conf_file, installroot=installroot)
            else:
                installed = is_installed(module, repoq, pkg, conf_file, en_repos=en_repos, dis_repos=dis_repos, installroot=installroot)
            if installed:
                module.fail_json(**res)
        res['changed'] = True
    return res
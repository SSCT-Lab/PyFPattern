def ensure(module, state, pkgs, conf_file, enablerepo, disablerepo, disable_gpg_check, exclude, repoq, installroot='/'):
    if module.get_bin_path('yum-deprecated'):
        yumbin = module.get_bin_path('yum-deprecated')
    else:
        yumbin = module.get_bin_path('yum')
    yum_basecmd = [yumbin, '-d', '2', '-y']
    if (conf_file and os.path.exists(conf_file)):
        yum_basecmd += ['-c', conf_file]
        if repoq:
            repoq += ['-c', conf_file]
    dis_repos = []
    en_repos = []
    if disablerepo:
        dis_repos = disablerepo.split(',')
        r_cmd = [('--disablerepo=%s' % disablerepo)]
        yum_basecmd.extend(r_cmd)
    if enablerepo:
        en_repos = enablerepo.split(',')
        r_cmd = [('--enablerepo=%s' % enablerepo)]
        yum_basecmd.extend(r_cmd)
    if exclude:
        e_cmd = [('--exclude=%s' % exclude)]
        yum_basecmd.extend(e_cmd)
    if (installroot != '/'):
        e_cmd = [('--installroot=%s' % installroot)]
        yum_basecmd.extend(e_cmd)
    if (state in ['installed', 'present', 'latest']):
        if module.params.get('update_cache'):
            module.run_command((yum_basecmd + ['clean', 'expire-cache']))
        my = yum_base(conf_file, installroot)
        try:
            if disablerepo:
                my.repos.disableRepo(disablerepo)
            current_repos = my.repos.repos.keys()
            if enablerepo:
                try:
                    my.repos.enableRepo(enablerepo)
                    new_repos = my.repos.repos.keys()
                    for i in new_repos:
                        if (not (i in current_repos)):
                            rid = my.repos.getRepo(i)
                            a = rid.repoXML.repoid
                    current_repos = new_repos
                except yum.Errors.YumBaseError:
                    e = get_exception()
                    module.fail_json(msg=('Error setting/accessing repos: %s' % e))
        except yum.Errors.YumBaseError:
            e = get_exception()
            module.fail_json(msg=('Error accessing repos: %s' % e))
    if (state in ['installed', 'present']):
        if disable_gpg_check:
            yum_basecmd.append('--nogpgcheck')
        res = install(module, pkgs, repoq, yum_basecmd, conf_file, en_repos, dis_repos, installroot=installroot)
    elif (state in ['removed', 'absent']):
        res = remove(module, pkgs, repoq, yum_basecmd, conf_file, en_repos, dis_repos, installroot=installroot)
    elif (state == 'latest'):
        if disable_gpg_check:
            yum_basecmd.append('--nogpgcheck')
        res = latest(module, pkgs, repoq, yum_basecmd, conf_file, en_repos, dis_repos, installroot=installroot)
    else:
        module.fail_json(msg='we should never get here unless this all failed', changed=False, results='', errors='unexpected state')
    return res
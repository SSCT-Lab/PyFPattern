def ensure(module, state, pkgs, conf_file, enablerepo, disablerepo, disable_gpg_check, exclude, repoq, skip_broken, update_only, security, installroot='/', allow_downgrade=False, disable_plugin=None, enable_plugin=None):
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
    if skip_broken:
        yum_basecmd.extend(['--skip-broken'])
    if disablerepo:
        dis_repos = disablerepo.split(',')
        r_cmd = [('--disablerepo=%s' % disablerepo)]
        yum_basecmd.extend(r_cmd)
    if enablerepo:
        en_repos = enablerepo.split(',')
        r_cmd = [('--enablerepo=%s' % enablerepo)]
        yum_basecmd.extend(r_cmd)
    if enable_plugin:
        yum_basecmd.extend(['--enableplugin', ','.join(enable_plugin)])
    if disable_plugin:
        yum_basecmd.extend(['--disableplugin', ','.join(disable_plugin)])
    if exclude:
        e_cmd = [('--exclude=%s' % exclude)]
        yum_basecmd.extend(e_cmd)
    if (installroot != '/'):
        e_cmd = [('--installroot=%s' % installroot)]
        yum_basecmd.extend(e_cmd)
    if (state in ['installed', 'present', 'latest']):
        ' The need of this entire if conditional has to be chalanged\n            this function is the ensure function that is called\n            in the main section.\n\n            This conditional tends to disable/enable repo for\n            install present latest action, same actually\n            can be done for remove and absent action\n\n            As solution I would advice to cal\n            try: my.repos.disableRepo(disablerepo)\n            and\n            try: my.repos.enableRepo(enablerepo)\n            right before any yum_cmd is actually called regardless\n            of yum action.\n\n            Please note that enable/disablerepo options are general\n            options, this means that we can call those with any action\n            option.  https://linux.die.net/man/8/yum\n\n            This docstring will be removed together when issue: #21619\n            will be solved.\n\n            This has been triggered by: #19587\n        '
        if module.params.get('update_cache'):
            module.run_command((yum_basecmd + ['clean', 'expire-cache']))
        my = yum_base(conf_file, installroot, enable_plugin, disable_plugin)
        try:
            if disablerepo:
                my.repos.disableRepo(disablerepo)
            current_repos = my.repos.repos.keys()
            if enablerepo:
                try:
                    my.repos.enableRepo(enablerepo)
                    new_repos = my.repos.repos.keys()
                    for i in new_repos:
                        if (i not in current_repos):
                            rid = my.repos.getRepo(i)
                            a = rid.repoXML.repoid
                    current_repos = new_repos
                except yum.Errors.YumBaseError as e:
                    module.fail_json(msg=('Error setting/accessing repos: %s' % to_native(e)))
        except yum.Errors.YumBaseError as e:
            module.fail_json(msg=('Error accessing repos: %s' % to_native(e)))
    if (state in ['installed', 'present']):
        if disable_gpg_check:
            yum_basecmd.append('--nogpgcheck')
        res = install(module, pkgs, repoq, yum_basecmd, conf_file, en_repos, dis_repos, enable_plugin, disable_plugin, installroot=installroot, allow_downgrade=allow_downgrade)
    elif (state in ['removed', 'absent']):
        res = remove(module, pkgs, repoq, yum_basecmd, conf_file, en_repos, dis_repos, enable_plugin, disable_plugin, installroot=installroot)
    elif (state == 'latest'):
        if disable_gpg_check:
            yum_basecmd.append('--nogpgcheck')
        if security:
            yum_basecmd.append('--security')
        res = latest(module, pkgs, repoq, yum_basecmd, conf_file, en_repos, dis_repos, enable_plugin, disable_plugin, update_only, installroot=installroot)
    else:
        module.fail_json(msg='we should never get here unless this all failed', changed=False, results='', errors='unexpected state')
    return res
def ensure(self, repoq):
    pkgs = self.names
    if ((not self.names) and self.autoremove):
        pkgs = []
        self.state = 'absent'
    if (self.conf_file and os.path.exists(self.conf_file)):
        self.yum_basecmd += ['-c', self.conf_file]
    if repoq:
        repoq += ['-c', self.conf_file]
    if self.skip_broken:
        self.yum_basecmd.extend(['--skip-broken'])
    if self.disablerepo:
        self.yum_basecmd.extend([('--disablerepo=%s' % ','.join(self.disablerepo))])
    if self.enablerepo:
        self.yum_basecmd.extend([('--enablerepo=%s' % ','.join(self.enablerepo))])
    if self.enable_plugin:
        self.yum_basecmd.extend(['--enableplugin', ','.join(self.enable_plugin)])
    if self.disable_plugin:
        self.yum_basecmd.extend(['--disableplugin', ','.join(self.disable_plugin)])
    if self.exclude:
        e_cmd = [('--exclude=%s' % ','.join(self.exclude))]
        self.yum_basecmd.extend(e_cmd)
    if self.disable_excludes:
        self.yum_basecmd.extend([('--disableexcludes=%s' % self.disable_excludes)])
    if self.download_only:
        self.yum_basecmd.extend(['--downloadonly'])
    if (self.installroot != '/'):
        e_cmd = [('--installroot=%s' % self.installroot)]
        self.yum_basecmd.extend(e_cmd)
    if (self.state in ('installed', 'present', 'latest')):
        ' The need of this entire if conditional has to be chalanged\n                this function is the ensure function that is called\n                in the main section.\n\n                This conditional tends to disable/enable repo for\n                install present latest action, same actually\n                can be done for remove and absent action\n\n                As solution I would advice to cal\n                try: my.repos.disableRepo(disablerepo)\n                and\n                try: my.repos.enableRepo(enablerepo)\n                right before any yum_cmd is actually called regardless\n                of yum action.\n\n                Please note that enable/disablerepo options are general\n                options, this means that we can call those with any action\n                option.  https://linux.die.net/man/8/yum\n\n                This docstring will be removed together when issue: #21619\n                will be solved.\n\n                This has been triggered by: #19587\n            '
        if self.update_cache:
            self.module.run_command((self.yum_basecmd + ['clean', 'expire-cache']))
        my = self.yum_base()
        try:
            if self.disablerepo:
                my.repos.disableRepo(self.disablerepo)
            current_repos = my.repos.repos.keys()
            if self.enablerepo:
                try:
                    for rid in self.enablerepo:
                        my.repos.enableRepo(rid)
                    new_repos = my.repos.repos.keys()
                    for i in new_repos:
                        if (i not in current_repos):
                            rid = my.repos.getRepo(i)
                            a = rid.repoXML.repoid
                    current_repos = new_repos
                except yum.Errors.YumBaseError as e:
                    self.module.fail_json(msg=('Error setting/accessing repos: %s' % to_native(e)))
        except yum.Errors.YumBaseError as e:
            self.module.fail_json(msg=('Error accessing repos: %s' % to_native(e)))
    if (self.state in ('installed', 'present')):
        if self.disable_gpg_check:
            self.yum_basecmd.append('--nogpgcheck')
        res = self.install(pkgs, repoq)
    elif (self.state in ('removed', 'absent')):
        res = self.remove(pkgs, repoq)
    elif (self.state == 'latest'):
        if self.disable_gpg_check:
            self.yum_basecmd.append('--nogpgcheck')
        if self.security:
            self.yum_basecmd.append('--security')
        if self.bugfix:
            self.yum_basecmd.append('--bugfix')
        res = self.latest(pkgs, repoq)
    else:
        self.module.fail_json(msg='we should never get here unless this all failed', changed=False, results='', errors='unexpected state')
    return res
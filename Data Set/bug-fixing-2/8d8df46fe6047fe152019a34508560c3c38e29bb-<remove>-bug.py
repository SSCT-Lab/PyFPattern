

def remove(self, items, repoq):
    pkgs = []
    res = {
        
    }
    res['results'] = []
    res['msg'] = ''
    res['changed'] = False
    res['rc'] = 0
    for pkg in items:
        if pkg.startswith('@'):
            installed = self.is_group_env_installed(pkg)
        else:
            installed = self.is_installed(repoq, pkg)
        if installed:
            pkgs.append(pkg)
        else:
            res['results'].append(('%s is not installed' % pkg))
    if pkgs:
        if self.module.check_mode:
            self.module.exit_json(changed=True, results=res['results'], changes=dict(removed=pkgs))
        if self.autoremove:
            cmd = ((self.yum_basecmd + ['autoremove']) + pkgs)
        else:
            cmd = ((self.yum_basecmd + ['remove']) + pkgs)
        (rc, out, err) = self.module.run_command(cmd)
        res['rc'] = rc
        res['results'].append(out)
        res['msg'] = err
        if (rc != 0):
            if self.autoremove:
                if ('No such command' not in out):
                    self.module.fail_json(msg='Version of YUM too old for autoremove: Requires yum 3.4.3 (RHEL/CentOS 7+)')
            else:
                self.module.fail_json(**res)
        for pkg in pkgs:
            if pkg.startswith('@'):
                installed = self.is_group_env_installed(pkg)
            else:
                installed = self.is_installed(repoq, pkg)
            if installed:
                self.module.fail_json(**res)
        res['changed'] = True
    return res

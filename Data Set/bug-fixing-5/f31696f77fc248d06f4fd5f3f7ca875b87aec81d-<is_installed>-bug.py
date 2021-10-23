def is_installed(module, repoq, pkgspec, conf_file, qf=def_qf, en_repos=None, dis_repos=None, is_pkg=False, installroot='/'):
    if (en_repos is None):
        en_repos = []
    if (dis_repos is None):
        dis_repos = []
    if (not repoq):
        pkgs = []
        try:
            my = yum_base(conf_file, installroot)
            for rid in dis_repos:
                my.repos.disableRepo(rid)
            for rid in en_repos:
                my.repos.enableRepo(rid)
            (e, m, u) = my.rpmdb.matchPackageNames([pkgspec])
            pkgs = (e + m)
            if ((not pkgs) and (not is_pkg)):
                pkgs.extend(my.returnInstalledPackagesByDep(pkgspec))
        except Exception:
            e = get_exception()
            module.fail_json(msg=('Failure talking to yum: %s' % e))
        return [po_to_envra(p) for p in pkgs]
    else:
        global rpmbin
        if (not rpmbin):
            rpmbin = module.get_bin_path('rpm', required=True)
        cmd = [rpmbin, '-q', '--qf', qf, pkgspec]
        if (installroot != '/'):
            cmd.extend(['--root', installroot])
        lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
        (rc, out, err) = module.run_command(cmd, environ_update=lang_env)
        if ((rc != 0) and ('is not installed' not in out)):
            module.fail_json(msg=('Error from rpm: %s: %s' % (cmd, err)))
        if ('is not installed' in out):
            out = ''
        pkgs = [p for p in out.replace('(none)', '0').split('\n') if p.strip()]
        if ((not pkgs) and (not is_pkg)):
            cmd = [rpmbin, '-q', '--qf', qf, '--whatprovides', pkgspec]
            if (installroot != '/'):
                cmd.extend(['--root', installroot])
            (rc2, out2, err2) = module.run_command(cmd, environ_update=lang_env)
        else:
            (rc2, out2, err2) = (0, '', '')
        if ((rc2 != 0) and ('no package provides' not in out2)):
            module.fail_json(msg=('Error from rpm: %s: %s' % (cmd, (err + err2))))
        if ('no package provides' in out2):
            out2 = ''
        pkgs += [p for p in out2.replace('(none)', '0').split('\n') if p.strip()]
        return pkgs
    return []
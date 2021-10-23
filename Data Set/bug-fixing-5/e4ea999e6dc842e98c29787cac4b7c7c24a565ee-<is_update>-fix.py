def is_update(module, repoq, pkgspec, conf_file, qf=def_qf, en_repos=None, dis_repos=None, installroot='/'):
    if (en_repos is None):
        en_repos = []
    if (dis_repos is None):
        dis_repos = []
    if (not repoq):
        retpkgs = []
        pkgs = []
        updates = []
        try:
            my = yum_base(conf_file, installroot)
            for rid in dis_repos:
                my.repos.disableRepo(rid)
            for rid in en_repos:
                my.repos.enableRepo(rid)
            pkgs = (my.returnPackagesByDep(pkgspec) + my.returnInstalledPackagesByDep(pkgspec))
            if (not pkgs):
                (e, m, u) = my.pkgSack.matchPackageNames([pkgspec])
                pkgs = (e + m)
            updates = my.doPackageLists(pkgnarrow='updates').updates
        except Exception:
            e = get_exception()
            module.fail_json(msg=('Failure talking to yum: %s' % e))
        for pkg in pkgs:
            if (pkg in updates):
                retpkgs.append(pkg)
        return set([po_to_envra(p) for p in retpkgs])
    else:
        myrepoq = list(repoq)
        r_cmd = ['--disablerepo', ','.join(dis_repos)]
        myrepoq.extend(r_cmd)
        r_cmd = ['--enablerepo', ','.join(en_repos)]
        myrepoq.extend(r_cmd)
        cmd = (myrepoq + ['--pkgnarrow=updates', '--qf', qf, pkgspec])
        (rc, out, err) = module.run_command(cmd)
        if (rc == 0):
            return set([p for p in out.split('\n') if p.strip()])
        else:
            module.fail_json(msg=('Error from repoquery: %s: %s' % (cmd, err)))
    return set()
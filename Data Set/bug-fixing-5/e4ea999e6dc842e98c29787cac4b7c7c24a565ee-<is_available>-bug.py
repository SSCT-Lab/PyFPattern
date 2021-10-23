def is_available(module, repoq, pkgspec, conf_file, qf=def_qf, en_repos=None, dis_repos=None, installroot='/'):
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
            (e, m, u) = my.pkgSack.matchPackageNames([pkgspec])
            pkgs = (e + m)
            if (not pkgs):
                pkgs.extend(my.returnPackagesByDep(pkgspec))
        except Exception:
            e = get_exception()
            module.fail_json(msg=('Failure talking to yum: %s' % e))
        return [po_to_nevra(p) for p in pkgs]
    else:
        myrepoq = list(repoq)
        r_cmd = ['--disablerepo', ','.join(dis_repos)]
        myrepoq.extend(r_cmd)
        r_cmd = ['--enablerepo', ','.join(en_repos)]
        myrepoq.extend(r_cmd)
        cmd = (myrepoq + ['--qf', qf, pkgspec])
        (rc, out, err) = module.run_command(cmd)
        if (rc == 0):
            return [p for p in out.split('\n') if p.strip()]
        else:
            module.fail_json(msg=('Error from repoquery: %s: %s' % (cmd, err)))
    return []
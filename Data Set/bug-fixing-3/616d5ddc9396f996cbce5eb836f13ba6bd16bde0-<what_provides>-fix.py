def what_provides(module, repoq, req_spec, conf_file, qf=def_qf, en_repos=None, dis_repos=None, installroot='/'):
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
            pkgs = (my.returnPackagesByDep(req_spec) + my.returnInstalledPackagesByDep(req_spec))
            if (not pkgs):
                (e, m, u) = my.pkgSack.matchPackageNames([req_spec])
                pkgs.extend(e)
                pkgs.extend(m)
                (e, m, u) = my.rpmdb.matchPackageNames([req_spec])
                pkgs.extend(e)
                pkgs.extend(m)
        except Exception:
            e = get_exception()
            module.fail_json(msg=('Failure talking to yum: %s' % e))
        return set([po_to_nevra(p) for p in pkgs])
    else:
        myrepoq = list(repoq)
        r_cmd = ['--disablerepo', ','.join(dis_repos)]
        myrepoq.extend(r_cmd)
        r_cmd = ['--enablerepo', ','.join(en_repos)]
        myrepoq.extend(r_cmd)
        cmd = (myrepoq + ['--qf', qf, '--whatprovides', req_spec])
        (rc, out, err) = module.run_command(cmd)
        cmd = (myrepoq + ['--qf', qf, req_spec])
        (rc2, out2, err2) = module.run_command(cmd)
        if ((rc == 0) and (rc2 == 0)):
            out += out2
            pkgs = set([p for p in out.split('\n') if p.strip()])
            if (not pkgs):
                pkgs = is_installed(module, repoq, req_spec, conf_file, qf=qf, installroot=installroot)
            return pkgs
        else:
            module.fail_json(msg=('Error from repoquery: %s: %s' % (cmd, (err + err2))))
    return set()
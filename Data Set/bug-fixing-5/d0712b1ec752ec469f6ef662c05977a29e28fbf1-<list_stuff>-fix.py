def list_stuff(module, repoquerybin, conf_file, stuff, installroot='/', disablerepo='', enablerepo=''):
    qf = '%{name}|%{epoch}|%{version}|%{release}|%{arch}|%{repoid}'
    is_installed_qf = '%{name}|%{epoch}|%{version}|%{release}|%{arch}|installed\n'
    repoq = [repoquerybin, '--show-duplicates', '--plugins', '--quiet']
    if disablerepo:
        repoq.extend(['--disablerepo', disablerepo])
    if enablerepo:
        repoq.extend(['--enablerepo', enablerepo])
    if (installroot != '/'):
        repoq.extend(['--installroot', installroot])
    if (conf_file and os.path.exists(conf_file)):
        repoq += ['-c', conf_file]
    if (stuff == 'installed'):
        return [pkg_to_dict(p) for p in sorted(is_installed(module, repoq, '-a', conf_file, qf=is_installed_qf, installroot=installroot)) if p.strip()]
    elif (stuff == 'updates'):
        return [pkg_to_dict(p) for p in sorted(is_update(module, repoq, '-a', conf_file, qf=qf, installroot=installroot)) if p.strip()]
    elif (stuff == 'available'):
        return [pkg_to_dict(p) for p in sorted(is_available(module, repoq, '-a', conf_file, qf=qf, installroot=installroot)) if p.strip()]
    elif (stuff == 'repos'):
        return [dict(repoid=name, state='enabled') for name in sorted(repolist(module, repoq)) if name.strip()]
    else:
        return [pkg_to_dict(p) for p in sorted((is_installed(module, repoq, stuff, conf_file, qf=is_installed_qf, installroot=installroot) + is_available(module, repoq, stuff, conf_file, qf=qf, installroot=installroot))) if p.strip()]
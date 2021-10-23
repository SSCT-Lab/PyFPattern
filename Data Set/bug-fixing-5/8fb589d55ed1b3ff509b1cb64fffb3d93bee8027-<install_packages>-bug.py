def install_packages(module, pkgng_path, packages, cached, pkgsite, dir_arg, state):
    install_c = 0
    old_pkgng = pkgng_older_than(module, pkgng_path, [1, 1, 4])
    if (pkgsite != ''):
        if old_pkgng:
            pkgsite = ('PACKAGESITE=%s' % pkgsite)
        else:
            pkgsite = ('-r %s' % pkgsite)
    batch_var = 'env BATCH=yes'
    if ((not module.check_mode) and (not cached)):
        if old_pkgng:
            (rc, out, err) = module.run_command(('%s %s update' % (pkgsite, pkgng_path)))
        else:
            (rc, out, err) = module.run_command(('%s %s update' % (pkgng_path, dir_arg)))
        if (rc != 0):
            module.fail_json(msg='Could not update catalogue')
    for package in packages:
        already_installed = query_package(module, pkgng_path, package, dir_arg)
        if (already_installed and (state == 'present')):
            continue
        update_available = query_update(module, pkgng_path, package, dir_arg, old_pkgng, pkgsite)
        if ((not update_available) and already_installed and (state == 'latest')):
            continue
        if (not module.check_mode):
            if already_installed:
                action = 'upgrade'
            else:
                action = 'install'
            if old_pkgng:
                (rc, out, err) = module.run_command(('%s %s %s %s -g -U -y %s' % (batch_var, pkgsite, pkgng_path, action, package)))
            else:
                (rc, out, err) = module.run_command(('%s %s %s %s %s -g -U -y %s' % (batch_var, pkgng_path, dir_arg, action, pkgsite, package)))
        if ((not module.check_mode) and (not query_package(module, pkgng_path, package, dir_arg))):
            module.fail_json(msg=('failed to %s %s: %s' % (action, package, out)), stderr=err)
        install_c += 1
    if (install_c > 0):
        return (True, ('added %s package(s)' % install_c))
    return (False, ('package(s) already %s' % state))
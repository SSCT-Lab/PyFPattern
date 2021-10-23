def ensure(module, base, state, names, autoremove):
    failures = []
    allow_erasing = False
    if ((not names) and autoremove):
        names = []
        state = 'absent'
    if ((names == ['*']) and (state == 'latest')):
        base.upgrade_all()
    else:
        (pkg_specs, group_specs, filenames) = _parse_spec_group_file(names)
        if group_specs:
            base.read_comps()
        pkg_specs = [p.strip() for p in pkg_specs]
        filenames = [f.strip() for f in filenames]
        groups = []
        environments = []
        for group_spec in (g.strip() for g in group_specs):
            group = base.comps.group_by_pattern(group_spec)
            if group:
                groups.append(group.id)
            else:
                environment = base.comps.environment_by_pattern(group_spec)
                if environment:
                    environments.append(environment.id)
                else:
                    base.close()
                    module.fail_json(msg='No group {0} available.'.format(group_spec))
        if (state in ['installed', 'present']):
            _install_remote_rpms(base, filenames)
            for group in groups:
                try:
                    base.group_install(group, dnf.const.GROUP_PACKAGE_TYPES)
                except dnf.exceptions.Error as e:
                    failures.append((group, to_native(e)))
            for environment in environments:
                try:
                    base.environment_install(environment, dnf.const.GROUP_PACKAGE_TYPES)
                except dnf.exceptions.Error as e:
                    failures.append((environment, to_native(e)))
            for pkg_spec in pkg_specs:
                _mark_package_install(module, base, pkg_spec)
        elif (state == 'latest'):
            _install_remote_rpms(base, filenames)
            for group in groups:
                try:
                    try:
                        base.group_upgrade(group)
                    except dnf.exceptions.CompsError:
                        base.group_install(group, dnf.const.GROUP_PACKAGE_TYPES)
                except dnf.exceptions.Error as e:
                    failures.append((group, to_native(e)))
            for environment in environments:
                try:
                    try:
                        base.environment_upgrade(environment)
                    except dnf.exceptions.CompsError:
                        base.environment_install(environment, dnf.const.GROUP_PACKAGE_TYPES)
                except dnf.exceptions.Error as e:
                    failures.append((environment, to_native(e)))
            for pkg_spec in pkg_specs:
                base.conf.best = True
                try:
                    base.install(pkg_spec)
                except dnf.exceptions.MarkingError as e:
                    failures.append((pkg_spec, to_native(e)))
        else:
            if autoremove:
                base.conf.clean_requirements_on_remove = autoremove
            if filenames:
                base.close()
                module.fail_json(msg='Cannot remove paths -- please specify package name.')
            for group in groups:
                try:
                    base.group_remove(group)
                except dnf.exceptions.CompsError:
                    pass
            for environment in environments:
                try:
                    base.environment_remove(environment)
                except dnf.exceptions.CompsError:
                    pass
            installed = base.sack.query().installed()
            for pkg_spec in pkg_specs:
                if installed.filter(name=pkg_spec):
                    base.remove(pkg_spec)
            allow_erasing = True
            if autoremove:
                base.autoremove()
    if (not base.resolve(allow_erasing=allow_erasing)):
        if failures:
            base.close()
            module.fail_json(msg='Failed to install some of the specified packages', failures=failures)
        base.close()
        module.exit_json(msg='Nothing to do')
    else:
        if module.check_mode:
            if failures:
                base.close()
                module.fail_json(msg='Failed to install some of the specified packages', failures=failures)
            base.close()
            module.exit_json(changed=True)
        base.download_packages(base.transaction.install_set)
        base.do_transaction()
        response = {
            'changed': True,
            'results': [],
        }
        for package in base.transaction.install_set:
            response['results'].append('Installed: {0}'.format(package))
        for package in base.transaction.remove_set:
            response['results'].append('Removed: {0}'.format(package))
        if failures:
            base.close()
            module.fail_json(msg='Failed to install some of the specified packages', failures=failures)
        base.close()
        module.exit_json(**response)
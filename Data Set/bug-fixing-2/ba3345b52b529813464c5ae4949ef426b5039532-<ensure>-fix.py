

def ensure(self):
    allow_erasing = False
    response = {
        'msg': '',
        'changed': False,
        'results': [],
        'rc': 0,
    }
    failure_response = {
        'msg': '',
        'failures': [],
        'results': [],
        'rc': 1,
    }
    if ((not self.names) and self.autoremove):
        self.names = []
        self.state = 'absent'
    if ((self.names == ['*']) and (self.state == 'latest')):
        try:
            self.base.upgrade_all()
        except dnf.exceptions.DepsolveError as e:
            failure_response['msg'] = 'Depsolve Error occured attempting to upgrade all packages'
            self.module.fail_json(**failure_response)
    else:
        (pkg_specs, group_specs, module_specs, filenames) = self._parse_spec_group_file()
        pkg_specs = [p.strip() for p in pkg_specs]
        filenames = [f.strip() for f in filenames]
        groups = []
        environments = []
        for group_spec in (g.strip() for g in group_specs):
            group = self.base.comps.group_by_pattern(group_spec)
            if group:
                groups.append(group.id)
            else:
                environment = self.base.comps.environment_by_pattern(group_spec)
                if environment:
                    environments.append(environment.id)
                else:
                    self.module.fail_json(msg='No group {0} available.'.format(group_spec), results=[])
        if (self.state in ['installed', 'present']):
            self._install_remote_rpms(filenames)
            for filename in filenames:
                response['results'].append('Installed {0}'.format(filename))
            if (module_specs and self.with_modules):
                for module in module_specs:
                    try:
                        if (not self._is_module_installed(module)):
                            response['results'].append('Module {0} installed.'.format(module))
                        self.module_base.install([module])
                    except dnf.exceptions.MarkingErrors as e:
                        failure_response['failures'].append(' '.join((' '.join(module), to_native(e))))
            for group in groups:
                try:
                    group_pkg_count_installed = self.base.group_install(group, dnf.const.GROUP_PACKAGE_TYPES)
                    if (group_pkg_count_installed == 0):
                        response['results'].append('Group {0} already installed.'.format(group))
                    else:
                        response['results'].append('Group {0} installed.'.format(group))
                except dnf.exceptions.DepsolveError as e:
                    failure_response['msg'] = 'Depsolve Error occured attempting to install group: {0}'.format(group)
                    self.module.fail_json(**failure_response)
                except dnf.exceptions.Error as e:
                    failure_response['failures'].append(' '.join((group, to_native(e))))
            for environment in environments:
                try:
                    self.base.environment_install(environment, dnf.const.GROUP_PACKAGE_TYPES)
                except dnf.exceptions.DepsolveError as e:
                    failure_response['msg'] = 'Depsolve Error occured attempting to install environment: {0}'.format(environment)
                    self.module.fail_json(**failure_response)
                except dnf.exceptions.Error as e:
                    failure_response['failures'].append(' '.join((environment, to_native(e))))
            if (module_specs and (not self.with_modules)):
                self.module.fail_json(msg='No group {0} available.'.format(module_specs[0]), results=[])
            if self.update_only:
                not_installed = self._update_only(pkg_specs)
                for spec in not_installed:
                    response['results'].append(('Packages providing %s not installed due to update_only specified' % spec))
            else:
                for pkg_spec in pkg_specs:
                    install_result = self._mark_package_install(pkg_spec)
                    if install_result['failed']:
                        failure_response['msg'] += install_result['msg']
                        failure_response['failures'].append(self._sanitize_dnf_error_msg(pkg_spec, install_result['failure']))
                    else:
                        response['results'].append(install_result['msg'])
        elif (self.state == 'latest'):
            self._install_remote_rpms(filenames)
            for filename in filenames:
                response['results'].append('Installed {0}'.format(filename))
            if (module_specs and self.with_modules):
                for module in module_specs:
                    try:
                        if self._is_module_installed(module):
                            response['results'].append('Module {0} upgraded.'.format(module))
                        self.module_base.upgrade([module])
                    except dnf.exceptions.MarkingErrors as e:
                        failure_response['failures'].append(' '.join((' '.join(module), to_native(e))))
            for group in groups:
                try:
                    try:
                        self.base.group_upgrade(group)
                        response['results'].append('Group {0} upgraded.'.format(group))
                    except dnf.exceptions.CompsError:
                        if (not self.update_only):
                            group_pkg_count_installed = self.base.group_install(group, dnf.const.GROUP_PACKAGE_TYPES)
                            if (group_pkg_count_installed == 0):
                                response['results'].append('Group {0} already installed.'.format(group))
                            else:
                                response['results'].append('Group {0} installed.'.format(group))
                except dnf.exceptions.Error as e:
                    failure_response['failures'].append(' '.join((group, to_native(e))))
            for environment in environments:
                try:
                    try:
                        self.base.environment_upgrade(environment)
                    except dnf.exceptions.CompsError:
                        self.base.environment_install(environment, dnf.const.GROUP_PACKAGE_TYPES)
                except dnf.exceptions.DepsolveError as e:
                    failure_response['msg'] = 'Depsolve Error occured attempting to install environment: {0}'.format(environment)
                except dnf.exceptions.Error as e:
                    failure_response['failures'].append(' '.join((environment, to_native(e))))
            if self.update_only:
                not_installed = self._update_only(pkg_specs)
                for spec in not_installed:
                    response['results'].append(('Packages providing %s not installed due to update_only specified' % spec))
            else:
                for pkg_spec in pkg_specs:
                    self.base.conf.best = True
                    install_result = self._mark_package_install(pkg_spec, upgrade=True)
                    if install_result['failed']:
                        failure_response['msg'] += install_result['msg']
                        failure_response['failures'].append(self._sanitize_dnf_error_msg(pkg_spec, install_result['failure']))
                    else:
                        response['results'].append(install_result['msg'])
        else:
            if filenames:
                self.module.fail_json(msg='Cannot remove paths -- please specify package name.', results=[])
            if (module_specs and self.with_modules):
                for module in module_specs:
                    try:
                        if self._is_module_installed(module):
                            response['results'].append('Module {0} removed.'.format(module))
                        self.module_base.disable([module])
                        self.module_base.remove([module])
                    except dnf.exceptions.MarkingErrors as e:
                        failure_response['failures'].append(' '.join((' '.join(module), to_native(e))))
            for group in groups:
                try:
                    self.base.group_remove(group)
                except dnf.exceptions.CompsError:
                    pass
                except AttributeError:
                    pass
            for environment in environments:
                try:
                    self.base.environment_remove(environment)
                except dnf.exceptions.CompsError:
                    pass
            installed = self.base.sack.query().installed()
            for pkg_spec in pkg_specs:
                installed_pkg = list(map(str, installed.filter(name=pkg_spec).run()))
                if installed_pkg:
                    candidate_pkg = self._packagename_dict(installed_pkg[0])
                    installed_pkg = installed.filter(name=candidate_pkg['name']).run()
                else:
                    candidate_pkg = self._packagename_dict(pkg_spec)
                    installed_pkg = installed.filter(nevra=pkg_spec).run()
                if installed_pkg:
                    installed_pkg = installed_pkg[0]
                    evr_cmp = self._compare_evr(installed_pkg.epoch, installed_pkg.version, installed_pkg.release, candidate_pkg['epoch'], candidate_pkg['version'], candidate_pkg['release'])
                    if (evr_cmp == 0):
                        self.base.remove(pkg_spec)
            allow_erasing = True
            if self.autoremove:
                self.base.autoremove()
    try:
        if (not self.base.resolve(allow_erasing=allow_erasing)):
            if failure_response['failures']:
                failure_response['msg'] = 'Failed to install some of the specified packages'
                self.module.fail_json(**failure_response)
            response['msg'] = 'Nothing to do'
            self.module.exit_json(**response)
        else:
            response['changed'] = True
            if failure_response['failures']:
                failure_response['msg'] = ('Failed to install some of the specified packages',)
                self.module.fail_json(**failure_response)
            if self.module.check_mode:
                response['msg'] = 'Check mode: No changes made, but would have if not in check mode'
                self.module.exit_json(**response)
            try:
                if (self.download_only and self.download_dir and self.base.conf.destdir):
                    dnf.util.ensure_dir(self.base.conf.destdir)
                    self.base.repos.all().pkgdir = self.base.conf.destdir
                self.base.download_packages(self.base.transaction.install_set)
            except dnf.exceptions.DownloadError as e:
                self.module.fail_json(msg='Failed to download packages: {0}'.format(to_text(e)), results=[])
            if self.download_only:
                for package in self.base.transaction.install_set:
                    response['results'].append('Downloaded: {0}'.format(package))
                self.module.exit_json(**response)
            else:
                self.base.do_transaction()
                for package in self.base.transaction.install_set:
                    response['results'].append('Installed: {0}'.format(package))
                for package in self.base.transaction.remove_set:
                    response['results'].append('Removed: {0}'.format(package))
            if failure_response['failures']:
                failure_response['msg'] = ('Failed to install some of the specified packages',)
                self.module.exit_json(**response)
            self.module.exit_json(**response)
    except dnf.exceptions.DepsolveError as e:
        failure_response['msg'] = 'Depsolve Error occured: {0}'.format(to_native(e))
        self.module.fail_json(**failure_response)
    except dnf.exceptions.Error as e:
        if (to_text('already installed') in to_text(e)):
            response['changed'] = False
            response['results'].append('Package already installed: {0}'.format(to_native(e)))
            self.module.exit_json(**response)
        else:
            failure_response['msg'] = 'Unknown Error occured: {0}'.format(to_native(e))
            self.module.fail_json(**failure_response)

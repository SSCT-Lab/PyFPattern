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
        (pkg_specs, group_specs, env_specs, module_specs, filenames) = self._parse_spec_group_file()
        pkg_specs = [p.strip() for p in pkg_specs]
        filenames = [f.strip() for f in filenames]
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
            for group in group_specs:
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
            for environment in env_specs:
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
            for group in group_specs:
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
            for environment in env_specs:
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
            for group in group_specs:
                try:
                    self.base.group_remove(group)
                except dnf.exceptions.CompsError:
                    pass
                except AttributeError:
                    pass
            for environment in env_specs:
                try:
                    self.base.environment_remove(environment)
                except dnf.exceptions.CompsError:
                    pass
            installed = self.base.sack.query().installed()
            for pkg_spec in pkg_specs:
                if (('*' in pkg_spec) or installed.filter(name=pkg_spec)):
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
            if self.module.check_mode:
                if failure_response['failures']:
                    failure_response['msg'] = ('Failed to install some of the specified packages',)
                    self.module.fail_json(**failure_response)
                response['msg'] = 'Check mode: No changes made, but would have if not in check mode'
                self.module.exit_json(**response)
            try:
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
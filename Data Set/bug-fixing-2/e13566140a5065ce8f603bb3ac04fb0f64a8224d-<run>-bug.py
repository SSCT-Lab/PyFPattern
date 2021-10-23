

def run(self):
    '\n        actually execute the module code backend\n        '
    error_msgs = []
    if (not HAS_RPM_PYTHON):
        error_msgs.append('The Python 2 bindings for rpm are needed for this module. If you require Python 3 support use the `dnf` Ansible module instead.')
    if (not HAS_YUM_PYTHON):
        error_msgs.append('The Python 2 yum module is needed for this module. If you require Python 3 support use the `dnf` Ansible module instead.')
    self.wait_for_lock()
    if error_msgs:
        self.module.fail_json(msg='. '.join(error_msgs))
    if (self.update_cache and (not self.names) and (not self.list)):
        (rc, stdout, stderr) = self.module.run_command((self.yum_basecmd + ['clean', 'expire-cache']))
        if (rc == 0):
            self.module.exit_json(changed=False, msg='Cache updated', rc=rc, results=[])
        else:
            self.module.exit_json(changed=False, msg='Failed to update cache', rc=rc, results=[stderr])
    if self.module.get_bin_path('yum-deprecated'):
        yumbin = self.module.get_bin_path('yum-deprecated')
    else:
        yumbin = self.module.get_bin_path('yum')
    self.yum_basecmd = [yumbin, '-d', '2', '-y']
    repoquerybin = self.module.get_bin_path('repoquery', required=False)
    if (self.install_repoquery and (not repoquerybin) and (not self.module.check_mode)):
        yum_path = self.module.get_bin_path('yum')
        if yum_path:
            self.module.run_command(('%s -y install yum-utils' % yum_path))
        repoquerybin = self.module.get_bin_path('repoquery', required=False)
    if self.list:
        if (not repoquerybin):
            self.module.fail_json(msg='repoquery is required to use list= with this module. Please install the yum-utils package.')
        results = {
            'results': self.list_stuff(repoquerybin, self.list),
        }
    else:
        my = self.yum_base()
        my.conf
        repoquery = None
        try:
            yum_plugins = my.plugins._plugins
        except AttributeError:
            pass
        else:
            if ('rhnplugin' in yum_plugins):
                if repoquerybin:
                    repoquery = [repoquerybin, '--show-duplicates', '--plugins', '--quiet']
                    if (self.installroot != '/'):
                        repoquery.extend(['--installroot', self.installroot])
                    if self.disable_excludes:
                        try:
                            with open('/etc/yum.conf', 'r') as f:
                                content = f.readlines()
                            tmp_conf_file = tempfile.NamedTemporaryFile(dir=self.module.tmpdir, delete=False)
                            self.module.add_cleanup_file(tmp_conf_file.name)
                            tmp_conf_file.writelines([c for c in content if (not c.startswith('exclude='))])
                            tmp_conf_file.close()
                        except Exception as e:
                            self.module.fail_json(msg=('Failure setting up repoquery: %s' % to_native(e)))
                        repoquery.extend(['-c', tmp_conf_file.name])
        results = self.ensure(repoquery)
        if repoquery:
            results['msg'] = ('%s %s' % (results.get('msg', ''), 'Warning: Due to potential bad behaviour with rhnplugin and certificates, used slower repoquery calls instead of Yum API.'))
    self.module.exit_json(**results)

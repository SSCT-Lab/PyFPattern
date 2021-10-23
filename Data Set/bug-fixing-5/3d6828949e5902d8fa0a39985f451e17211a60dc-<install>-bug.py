def install(self):
    changed = False
    plugin_file = ('%s/plugins/%s.jpi' % (self.params['jenkins_home'], self.params['name']))
    if ((not self.is_installed) and (self.params['version'] is None)):
        if (not self.module.check_mode):
            install_script = ('d = Jenkins.instance.updateCenter.getPlugin("%s").deploy(); d.get();' % self.params['name'])
            if self.params['with_dependencies']:
                install_script = ('Jenkins.instance.updateCenter.getPlugin("%s").getNeededDependencies().each{it.deploy()}; %s' % (self.params['name'], install_script))
            script_data = {
                'script': install_script,
            }
            script_data.update(self.crumb)
            data = urlencode(script_data)
            r = self._get_url_data(('%s/scriptText' % self.url), msg_status='Cannot install plugin.', msg_exception='Plugin installation has failed.', data=data)
            hpi_file = ('%s/plugins/%s.hpi' % (self.params['jenkins_home'], self.params['name']))
            if os.path.isfile(hpi_file):
                os.remove(hpi_file)
        changed = True
    else:
        if (not os.path.isdir(self.params['jenkins_home'])):
            self.module.fail_json(msg="Jenkins home directory doesn't exist.")
        md5sum_old = None
        if os.path.isfile(plugin_file):
            md5sum_old = hashlib.md5(open(plugin_file, 'rb').read()).hexdigest()
        if (self.params['version'] in [None, 'latest']):
            plugin_url = ('%s/latest/%s.hpi' % (self.params['updates_url'], self.params['name']))
        else:
            plugin_url = '{0}/download/plugins/{1}/{2}/{1}.hpi'.format(self.params['updates_url'], self.params['name'], self.params['version'])
        if ((self.params['updates_expiration'] == 0) or (self.params['version'] not in [None, 'latest']) or (md5sum_old is None)):
            r = self._download_plugin(plugin_url)
            if (md5sum_old is None):
                if (not self.module.check_mode):
                    self._write_file(plugin_file, r)
                changed = True
            else:
                data = r.read()
                md5sum_new = hashlib.md5(data).hexdigest()
                if (md5sum_old != md5sum_new):
                    if (not self.module.check_mode):
                        self._write_file(plugin_file, data)
                    changed = True
        else:
            plugin_data = self._download_updates()
            try:
                sha1_old = hashlib.sha1(open(plugin_file, 'rb').read())
            except Exception as e:
                self.module.fail_json(msg='Cannot calculate SHA1 of the old plugin.', details=to_native(e))
            sha1sum_old = base64.b64encode(sha1_old.digest())
            if (sha1sum_old != plugin_data['sha1']):
                if (not self.module.check_mode):
                    r = self._download_plugin(plugin_url)
                    self._write_file(plugin_file, r)
                changed = True
    if os.path.isfile(plugin_file):
        params = {
            'dest': plugin_file,
        }
        params.update(self.params)
        file_args = self.module.load_file_common_arguments(params)
        if (not self.module.check_mode):
            changed = self.module.set_fs_attributes_if_different(file_args, changed)
        else:
            changed = True
    return changed
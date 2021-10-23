

def _configure_base(self, base, conf_file, disable_gpg_check, installroot='/'):
    'Configure the dnf Base object.'
    if (self.enable_plugin and self.disable_plugin):
        base.init_plugins(self.disable_plugin, self.enable_plugin)
    elif self.enable_plugin:
        base.init_plugins(enable_plugins=self.enable_plugin)
    elif self.disable_plugin:
        base.init_plugins(self.disable_plugin)
    conf = base.conf
    conf.debuglevel = 0
    conf.gpgcheck = (not disable_gpg_check)
    conf.assumeyes = True
    conf.installroot = installroot
    if self.exclude:
        conf.exclude(self.exclude)
    if self.disable_excludes:
        conf.disable_excludes.append(self.disable_excludes)
    if (self.releasever is not None):
        conf.substitutions['releasever'] = self.releasever
    if self.skip_broken:
        conf.strict = 0
    if self.download_only:
        conf.downloadonly = True
    if conf_file:
        if (not os.access(conf_file, os.R_OK)):
            self.module.fail_json(msg='cannot read configuration file', conf_file=conf_file, results=[])
        else:
            conf.config_file_path = conf_file
    conf.clean_requirements_on_remove = self.autoremove
    conf.read()

def update_plugin_conf(self, plugin, enabled=True):
    plugin_conf = ('/etc/yum/pluginconf.d/%s.conf' % plugin)
    if os.path.isfile(plugin_conf):
        cfg = configparser.ConfigParser()
        cfg.read([plugin_conf])
        if enabled:
            cfg.set('main', 'enabled', 1)
        else:
            cfg.set('main', 'enabled', 0)
        fd = open(plugin_conf, 'rwa+')
        cfg.write(fd)
        fd.close()


def load_config(self):
    "(internal) This function is used for returning a ConfigParser with\n        the application configuration. It's doing 3 things:\n\n            #. Creating an instance of a ConfigParser\n            #. Loading the default configuration by calling\n               :meth:`build_config`, then\n            #. If it exists, it loads the application configuration file,\n               otherwise it creates one.\n\n        :return:\n            :class:`~kivy.config.ConfigParser` instance\n        "
    try:
        config = ConfigParser.get_configparser('app')
    except KeyError:
        config = None
    if (config is None):
        config = ConfigParser(name='app')
    self.config = config
    self.build_config(config)
    filename = self.get_application_config()
    if (not filename):
        if config.sections():
            return config
        return
    Logger.debug('App: Loading configuration <{0}>'.format(filename))
    if exists(filename):
        try:
            config.read(filename)
        except:
            Logger.error('App: Corrupted config file, ignored.')
            config.name = ''
            try:
                config = ConfigParser.get_configparser('app')
            except KeyError:
                config = None
            if (config is None):
                config = ConfigParser(name='app')
            self.config = config
            self.build_config(config)
            pass
    else:
        Logger.debug('App: First configuration, create <{0}>'.format(filename))
        config.filename = filename
        config.write()
    return config

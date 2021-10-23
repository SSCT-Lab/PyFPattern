def read_settings(self):
    ' Reads the settings from the vmware_inventory.ini file '
    scriptbasename = os.path.realpath(__file__)
    scriptbasename = os.path.basename(scriptbasename)
    scriptbasename = scriptbasename.replace('.py', '')
    defaults = {
        'vmware': {
            'server': '',
            'port': 443,
            'username': '',
            'password': '',
            'ini_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), ('%s.ini' % scriptbasename)),
            'cache_name': 'ansible-vmware',
            'cache_path': '~/.ansible/tmp',
            'cache_max_age': 3600,
            'max_object_level': 1,
            'alias_pattern': '{{ config.name + "_" + config.uuid }}',
            'host_pattern': '{{ guest.ipaddress }}',
            'host_filters': '{{ guest.gueststate == "running" }}',
            'groupby_patterns': '{{ guest.guestid }},{{ "templates" if config.template else "guests"}}',
            'lower_var_keys': True,
        },
    }
    if six.PY3:
        config = configparser.ConfigParser()
    else:
        config = configparser.SafeConfigParser()
    vmware_ini_path = os.environ.get('VMWARE_INI_PATH', defaults['vmware']['ini_path'])
    vmware_ini_path = os.path.expanduser(os.path.expandvars(vmware_ini_path))
    config.read(vmware_ini_path)
    for (k, v) in defaults['vmware'].iteritems():
        if (not config.has_option('vmware', k)):
            config.set('vmware', k, str(v))
    self.cache_dir = os.path.expanduser(config.get('vmware', 'cache_path'))
    if (self.cache_dir and (not os.path.exists(self.cache_dir))):
        os.makedirs(self.cache_dir)
    cache_name = config.get('vmware', 'cache_name')
    self.cache_path_cache = (self.cache_dir + ('/%s.cache' % cache_name))
    self.cache_max_age = int(config.getint('vmware', 'cache_max_age'))
    self.server = os.environ.get('VMWARE_SERVER', config.get('vmware', 'server'))
    self.port = int(os.environ.get('VMWARE_PORT', config.get('vmware', 'port')))
    self.username = os.environ.get('VMWARE_USERNAME', config.get('vmware', 'username'))
    self.password = os.environ.get('VMWARE_PASSWORD', config.get('vmware', 'password'))
    self.maxlevel = int(config.get('vmware', 'max_object_level'))
    self.lowerkeys = config.get('vmware', 'lower_var_keys')
    if (type(self.lowerkeys) != bool):
        if (str(self.lowerkeys).lower() in ['yes', 'true', '1']):
            self.lowerkeys = True
        else:
            self.lowerkeys = False
    self.host_filters = list(config.get('vmware', 'host_filters').split(','))
    self.groupby_patterns = list(config.get('vmware', 'groupby_patterns').split(','))
    self.config = config
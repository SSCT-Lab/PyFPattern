def read_settings(self):
    ' Reads the settings from the digital_ocean.ini file '
    config = ConfigParser.SafeConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'digital_ocean.ini')
    config.read(config_path)
    if config.has_option('digital_ocean', 'api_token'):
        self.api_token = config.get('digital_ocean', 'api_token')
    if config.has_option('digital_ocean', 'cache_path'):
        self.cache_path = config.get('digital_ocean', 'cache_path')
    if config.has_option('digital_ocean', 'cache_max_age'):
        self.cache_max_age = config.getint('digital_ocean', 'cache_max_age')
    if config.has_option('digital_ocean', 'use_private_network'):
        self.use_private_network = config.getboolean('digital_ocean', 'use_private_network')
    if config.has_option('digital_ocean', 'group_variables'):
        self.group_variables = ast.literal_eval(config.get('digital_ocean', 'group_variables'))
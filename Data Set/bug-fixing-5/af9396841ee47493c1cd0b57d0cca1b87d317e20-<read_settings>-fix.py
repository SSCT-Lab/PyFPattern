def read_settings(self):
    config = configparser.SafeConfigParser()
    conf_path = './zabbix.ini'
    if (not os.path.exists(conf_path)):
        conf_path = (os.path.dirname(os.path.realpath(__file__)) + '/zabbix.ini')
    if os.path.exists(conf_path):
        config.read(conf_path)
    if config.has_option('zabbix', 'server'):
        self.zabbix_server = config.get('zabbix', 'server')
    if config.has_option('zabbix', 'username'):
        self.zabbix_username = config.get('zabbix', 'username')
    if config.has_option('zabbix', 'password'):
        self.zabbix_password = config.get('zabbix', 'password')
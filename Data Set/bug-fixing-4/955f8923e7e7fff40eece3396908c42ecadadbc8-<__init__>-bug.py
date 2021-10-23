def __init__(self):
    self.defaultgroup = 'group_all'
    self.zabbix_server = None
    self.zabbix_username = None
    self.zabbix_password = None
    self.read_settings()
    self.read_cli()
    if (self.zabbix_server and self.zabbix_username):
        try:
            api = ZabbixAPI(server=self.zabbix_server)
            api.login(user=self.zabbix_username, password=self.zabbix_password)
        except BaseException as e:
            print('Error: Could not login to Zabbix server. Check your zabbix.ini.', file=sys.stderr)
            sys.exit(1)
        if self.options.host:
            data = self.get_host(api, self.options.host)
            print(json.dumps(data, indent=2))
        elif self.options.list:
            data = self.get_list(api)
            print(json.dumps(data, indent=2))
        else:
            print('usage: --list  ..OR.. --host <hostname>', file=sys.stderr)
            sys.exit(1)
    else:
        print('Error: Configuration of server and credentials are required. See zabbix.ini.', file=sys.stderr)
        sys.exit(1)
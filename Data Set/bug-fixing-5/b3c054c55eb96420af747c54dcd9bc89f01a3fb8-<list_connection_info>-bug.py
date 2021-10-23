def list_connection_info(self):
    bus = dbus.SystemBus()
    service_name = 'org.freedesktop.NetworkManager'
    settings = None
    try:
        proxy = bus.get_object(service_name, '/org/freedesktop/NetworkManager/Settings')
        settings = dbus.Interface(proxy, 'org.freedesktop.NetworkManager.Settings')
    except dbus.Exceptions.DBusException as e:
        self.module.fail_json(msg=('Unable to read Network Manager settings from DBus system bus: %s' % to_native(e)), details='Please check if NetworkManager is installed and service network-manager is started.')
    connection_paths = settings.ListConnections()
    connection_list = []
    for path in connection_paths:
        con_proxy = bus.get_object(service_name, path)
        settings_connection = dbus.Interface(con_proxy, 'org.freedesktop.NetworkManager.Settings.Connection')
        config = settings_connection.GetSettings()
        self.merge_secrets(settings_connection, config, '802-11-wireless')
        self.merge_secrets(settings_connection, config, '802-11-wireless-security')
        self.merge_secrets(settings_connection, config, '802-1x')
        self.merge_secrets(settings_connection, config, 'gsm')
        self.merge_secrets(settings_connection, config, 'cdma')
        self.merge_secrets(settings_connection, config, 'ppp')
        s_con = config['connection']
        connection_list.append(s_con['id'])
        connection_list.append(s_con['uuid'])
        connection_list.append(s_con['type'])
        connection_list.append(self.connection_to_string(config))
    return connection_list
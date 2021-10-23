def load_current_config(self):
    self._os_version = self._get_os_version()
    self._current_config = dict()
    config = self._get_interfaces_config()
    if (not config):
        return
    if (self._os_version < self.ONYX_API_VERSION):
        for if_data in config:
            if_name = self.get_if_name(if_data)
            self._current_config[if_name] = self._create_if_data(if_name, if_data)
    else:
        for if_config in config:
            for (if_name, if_data) in iteritems(if_config):
                if_data = if_data[0]
                self._current_config[if_name] = self._create_if_data(if_name, if_data)
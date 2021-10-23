

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
        if_data = dict()
        for if_config in config:
            for (if_name, if_attr) in iteritems(if_config):
                for config in if_attr:
                    for (key, value) in iteritems(config):
                        if_data[key] = value
                self._current_config[if_name] = self._create_if_data(if_name, if_data)

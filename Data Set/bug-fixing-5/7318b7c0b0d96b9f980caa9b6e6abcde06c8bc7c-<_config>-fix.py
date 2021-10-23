def _config(self):
    "Configure an LXC container.\n\n        Write new configuration values to the lxc config file. This will\n        stop the container if it's running write the new options and then\n        restart the container upon completion.\n        "
    _container_config = self.module.params.get('container_config')
    if (not _container_config):
        return False
    container_config_file = self.container.config_file_name
    with open(container_config_file, 'rb') as f:
        container_config = to_text(f.read(), errors='surrogate_or_strict').splitlines(True)
    import ast
    options_dict = ast.literal_eval(_container_config)
    parsed_options = [i.split('=', 1) for i in options_dict]
    config_change = False
    for (key, value) in parsed_options:
        key = key.strip()
        value = value.strip()
        new_entry = ('%s = %s\n' % (key, value))
        keyre = re.compile(('%s(\\s+)?=' % key))
        for option_line in container_config:
            if keyre.match(option_line):
                (_, _value) = option_line.split('=', 1)
                config_value = ' '.join(_value.split())
                line_index = container_config.index(option_line)
                if (value != config_value):
                    line_index += 1
                    if (new_entry not in container_config):
                        config_change = True
                        container_config.insert(line_index, new_entry)
                break
        else:
            config_change = True
            container_config.append(new_entry)
    if config_change:
        container_state = self._get_state()
        if (container_state != 'stopped'):
            self.container.stop()
        with open(container_config_file, 'wb') as f:
            f.writelines([to_bytes(line, errors='surrogate_or_strict') for line in container_config])
        self.state_change = True
        if (container_state == 'running'):
            self._container_startup()
        elif (container_state == 'frozen'):
            self._container_startup()
            self.container.freeze()